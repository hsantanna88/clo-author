/*===========================================================================
  01_build_panel.do
  Construye panel ENAHO 2004-2024 para análisis DiD

  Proyecto: Efectos de Ley 31110 sobre ingresos laborales agrícolas
  Datos:    ENAHO Módulo 500 (empleo e ingresos), INEI

  Grupos:
    Tratado: p506 ∈ {111,112,113,121,122,130,140} — cubiertos Ley 27360/31110
    Control: p506 ∈ {200,500,1512}                — excluidos de ambas leyes
===========================================================================*/

clear all
set more off

* Directorio raíz del proyecto (ajustar según máquina)
global root "C:\Users\GIrigoin\clo-author"
global raw  "$root\data\raw\enaho"
global clean "$root\data\cleaned"

* Años disponibles (agregar conforme se descargan)
local años 2004 2005 2006 2007 2008 2009 2010 2011 2012 ///
           2013 2014 2015 2016 2017 2018 2019 2020 2021 ///
           2022 2023 2024

* Crear archivo temporal para apilar
tempfile panel
save `panel', emptyok

/*---------------------------------------------------------------------------
  LOOP: procesar cada año y apilar
---------------------------------------------------------------------------*/
foreach y of local años {

    capture use "$raw\enaho01a-`y'-500.dta", clear
    if _rc != 0 {
        display as error "Archivo no encontrado: enaho01a-`y'-500.dta — saltando"
        continue
    }

    display "Procesando año `y'..."

    * Año
    gen anio = `y'

    * Grupos tratado y control
    gen tratado = inlist(p506, 111, 112, 113, 121, 122, 130, 140)
    gen control = inlist(p506, 200, 500, 1512)
    gen sector  = 1 if tratado == 1
    replace sector = 0 if control == 1
    keep if sector != .

    * Variable dependiente: ingreso laboral
    * NOTA: verificar nombre exacto con `lookfor ingreso` en cada año
    capture confirm variable i524a1
    if _rc == 0 rename i524a1 ingreso_laboral
    else {
        capture confirm variable p524a1
        if _rc == 0 rename p524a1 ingreso_laboral
        else {
            display as error "Variable de ingreso no encontrada en `y'"
            continue
        }
    }

    * Controles individuales
    capture rename p208a  edad
    capture rename p207   mujer
    capture rename p301a  educacion
    capture rename p209   estado_civil
    capture rename p510   nro_trabajadores  // proxy tamaño firma

    * Recodificar género: 1=hombre, 0=mujer
    capture recode mujer (1=0) (2=1), gen(es_mujer)

    * Mantener variables clave
    keep conglome vivienda hogar codperso anio sector tratado control ///
         ingreso_laboral edad es_mujer educacion estado_civil ///
         nro_trabajadores ocu500 factor07 ///
         dominio estrato

    append using `panel'
    save `panel', replace
}

/*---------------------------------------------------------------------------
  LIMPIEZA
---------------------------------------------------------------------------*/
use `panel', clear

* Solo ocupados con ingreso positivo
keep if ocu500 == 1
keep if ingreso_laboral > 0 & ingreso_laboral != .

* Log del ingreso (deflactar con IPC pendiente — ver 02_deflate.do)
gen log_ingreso = log(ingreso_laboral)

* Variable post-tratamiento
gen post = (anio >= 2021)

* Interacción DiD
gen did = tratado * post

* Indicador COVID
gen covid = inlist(anio, 2020, 2021)

* Edad al cuadrado
gen edad2 = edad^2

* Labels
label variable log_ingreso    "Log ingreso laboral mensual"
label variable tratado        "Sector agrícola (cubierto Ley 27360/31110)"
label variable control        "Sector control (excluido de ambas leyes)"
label variable post           "Post Ley 31110 (2021+)"
label variable did            "DiD: Tratado × Post"
label variable covid          "Período COVID (2020-2021)"
label variable es_mujer       "Mujer (=1)"

/*---------------------------------------------------------------------------
  GUARDAR
---------------------------------------------------------------------------*/
save "$clean\panel_enaho_2004_2024.dta", replace

display "Panel construido: `=_N' observaciones"
tab anio sector
