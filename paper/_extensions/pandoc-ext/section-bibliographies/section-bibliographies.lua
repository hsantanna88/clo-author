--- section-bibliographies - chapter-wise reference sections
---
--- Copyright: © 2018 Jesse Rosenthal, 2020–2024 Albert Krewinkel
--- License: MIT – see LICENSE for details

-- pandoc.utils.citeproc exists since pandoc 2.19.1
PANDOC_VERSION:must_be_at_least {2,19,1}

local List = require 'pandoc.List'
local utils = require 'pandoc.utils'
local citeproc, sha1, stringify = utils.citeproc, utils.sha1, utils.stringify
local make_sections = function (doc, opts)
  return utils.make_sections(opts.number_sections, nil, doc.blocks)
end
if PANDOC_VERSION >= '3.0' then
  make_sections = (require 'pandoc.structure').make_sections
end

-- Returns true iff a div is a section div.
local function is_section_div (div)
  return div.t == 'Div'
    and div.classes[1] == 'section'
    and (div.attributes.number or div.classes:includes 'unnumbered')
end

--- Returns the section heading when given a section div, and nil otherwise.
-- @param div   a pandoc Block element
-- @return heading element or nil
-- @return suffix to be used with identifiers
local function section_header (div)
  local header = div.content and div.content[1]
  local is_header = is_section_div(div)
    and header
    and header.t == 'Header'

  if not is_header then
    return nil, nil
  end

  local suffix = header.attributes.number or sha1(stringify(header.content))
  return header, '--' .. suffix
end

--- Unwrap and remove section divs
local function flatten_sections (div)
  local header = section_header(div)
  if not header then
    return nil
  else
    header.identifier = div.identifier
    header.attributes.number = nil
    div.content[1] = header
    return div.content
  end
end

local function adjust_refs_components (div)
  local header, suffix = section_header(div)
  if not header then
    return div
  end

  return div:walk {
    traverse = 'topdown',
    Header = function (h)
      if h.identifier == 'bibliography' then
        h.identifier = 'bibliography' .. suffix
        h.level = header.level + 1
        return h
      end
    end,
    Div = function (d)
      if d.identifier == 'refs' then
        d.identifier = 'refs' .. suffix
        return d
      end
    end
  }
end

--- Create a deep copy of a table.
-- Values that aren't tables are returned unchanged.
local function deepcopy (tbl)
  if type(tbl) ~= 'table' then
    return tbl
  end

  local copy = {}
  for k, v in pairs(tbl) do
    copy[k] = deepcopy(v)
  end
  return copy
end

-- negate a property
local negate = function (property)
  return function (x) return not property(x) end
end

--- Create a bibliography for a given section. This acts on all
-- section divs at or above `opts.level`
local function create_section_bibliography (meta, opts)
  local newmeta = deepcopy(meta)

  -- Load bibliography files just once.
  newmeta.bibliography = deepcopy(opts.bibliography)
  newmeta.references = deepcopy(opts.references)
  newmeta.nocite = pandoc.Inlines{
    pandoc.Cite('@*', {pandoc.Citation('*', 'NormalCitation')})
  }
  local references = utils.references(pandoc.Pandoc({}, newmeta))
  newmeta.bibliography = nil
  newmeta.nocite = nil

  -- Don't do anything if there is no bibliography
  if not next(references) then
    return nil
  end

  local function section_citeproc(section, suffix)
    section = pandoc.Blocks(section):walk{
      Cite = function (cite)
        cite.citations = cite.citations:map(function(c)
            c.id = c.id .. suffix
            return c
        end)
        return cite
      end,
      Div = function (div)
        if div.classes:includes 'sectionrefs' then
          div.identifier = 'refs'
          return div
        end
      end
    }
    newmeta.references = deepcopy(references)
    for i, ref in ipairs(newmeta.references) do
      newmeta.references[i].id = ref.id .. suffix
    end
    return citeproc(pandoc.Pandoc(section, newmeta)).blocks
  end

  local process_div
  process_div = function (div)
    local header, suffix = section_header(div)
    if not header or not suffix or opts.level < header.level then
      -- Don't do anything for deeply-nested sections.
      return div, false
    elseif header.level < opts.minlevel then
      -- Don't process sections above minlevel
      div.content = div.content:map(process_div)
      return div, false
    elseif opts.level == header.level then
      div.content = section_citeproc(div.content, suffix)
      return adjust_refs_components(div), false
    else
      -- Replace subsections, which we don't want to process, with
      -- placeholder blocks.
      local subsections = {}
      local subsection_to_placeholder = function (blk, i)
        local subh = section_header(blk)
        if subh and not subh.classes:includes 'sectionbibliography' then
          subsections[i] = blk
          return pandoc.RawBlock('placeholder', tostring(i))
        end
        return blk
      end
      -- replace placeholders with processed subsections
      local restore_from_placeholder = function (blk)
        if blk.t == 'RawBlock' and blk.format == 'placeholder' then
          return process_div(subsections[tonumber(blk.text)])
        end
        return blk
      end
      div.content = div.content:map(subsection_to_placeholder)
      div.content = section_citeproc(div.content, suffix)
      div.content = div.content:map(restore_from_placeholder)
      return adjust_refs_components(div), false
    end
  end

  return process_div
end

--- Filter to the references div and bibliography header added by
--- pandoc-citeproc.
local remove_pandoc_citeproc_results = {
  Header = function (header)
    return header.identifier == 'bibliography'
      and {}
      or nil
  end,
  Div = function (div)
    return div.identifier == 'refs'
      and {}
      or nil
  end
}

--- Create an options table from document metadata.
local function get_options (meta)
  local opts = meta['section-bibliographies'] or {}
  opts.bibliography = opts.bibliography
    or meta['section-bibs-bibliography']
    or meta['bibliography']
  opts.level = tonumber(opts.level)
    or tonumber(meta['section-bibs-level'])
    or 1
  opts.minlevel = tonumber(opts.minlevel)
    or 1
  opts.references = opts.references
    or meta['references']

  -- sanity check
  if opts.level < opts.minlevel then
    warn('level cannot be smaller than minlevel, setting minlevel = level')
    opts.minlevel = opts.level
  end

  return opts
end

return {
  {
    Pandoc = function (doc)
      local opts = get_options(doc.meta)
      if opts['cleanup-first'] then
        -- clear results of a previous citeproc run
        doc = doc:walk(remove_pandoc_citeproc_results)
      end
      -- Setup the document for further processing by wrapping all
      -- sections in Div elements, but undo that after.
      doc.blocks = make_sections(doc, {number_sections=true})
        :walk{
          traverse = 'topdown',
          Div = create_section_bibliography(doc.meta, opts)
        }
        :walk{Div = flatten_sections}
      return doc
    end
  }
}
