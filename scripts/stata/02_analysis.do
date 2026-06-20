/*===========================================================================
  02_analysis.do
  DiD principal y event study

  Requiere: data\cleaned\panel_enaho_2004_2024.dta
===========================================================================*/

clear all
set more off

global root "C:\Users\GIrigoin\clo-author"
global clean "$root\data\cleaned"
global figs  "$root\paper\figures"
global tabs  "$root\paper\tables"

* Instalar si es necesario
* ssc install reghdfe
* ssc install ftools
* ssc install coefplot
* ssc install estout

use "$clean\panel_enaho_2004_2024.dta", clear

local controles "edad edad2 es_mujer educacion"

/*---------------------------------------------------------------------------
  1. DiD PRINCIPAL
---------------------------------------------------------------------------*/
* Tabla con especificaciones progresivas
eststo clear

* (1) Solo FE año
eststo m1: reghdfe log_ingreso did, ///
    absorb(anio) vce(cluster conglome)

* (2) FE año + conglomerado
eststo m2: reghdfe log_ingreso did, ///
    absorb(anio conglome) vce(cluster conglome)

* (3) + controles individuales
eststo m3: reghdfe log_ingreso did `controles', ///
    absorb(anio conglome) vce(cluster conglome)

* (4) Excluir 2020-2021 (COVID)
eststo m4: reghdfe log_ingreso did `controles' if !covid, ///
    absorb(anio conglome) vce(cluster conglome)

esttab m1 m2 m3 m4 using "$tabs\did_main.tex", ///
    replace label booktabs ///
    title("Efecto de Ley 31110 sobre ingresos laborales agrícolas") ///
    mtitles("Solo FE año" "FE año+conglome" "+ Controles" "Sin COVID") ///
    keep(did) b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2_a, fmt(0 3) labels("Observaciones" "R2 ajustado"))

/*---------------------------------------------------------------------------
  2. EVENT STUDY
---------------------------------------------------------------------------*/
reghdfe log_ingreso ib2020.anio#i.tratado `controles', ///
    absorb(anio conglome) vce(cluster conglome)

estimates store event_study

* Gráfico
coefplot event_study, ///
    keep(*.anio#1.tratado) ///
    vertical ///
    yline(0, lcolor(red) lpattern(dash)) ///
    xline(17, lcolor(gs10) lpattern(dash)) ///
    ylabel(, format(%4.2f)) ///
    xlabel(, angle(45)) ///
    title("Event Study: Efecto de Ley 31110 sobre ingresos laborales") ///
    xtitle("Año") ytitle("Coeficiente (log ingreso, base=2020)") ///
    note("IC 95%. Errores estándar clusterizados a nivel conglomerado.") ///
    graphregion(color(white)) bgcolor(white)

graph export "$figs\event_study_main.pdf", replace

/*---------------------------------------------------------------------------
  3. HETEROGENEIDAD
---------------------------------------------------------------------------*/
* Por género
eststo clear
eststo hom: reghdfe log_ingreso did `controles' if es_mujer==0, ///
    absorb(anio conglome) vce(cluster conglome)
eststo muj: reghdfe log_ingreso did `controles' if es_mujer==1, ///
    absorb(anio conglome) vce(cluster conglome)

* Por región (dominio: 1=costa urbana, 2=sierra urbana, 3=selva urbana,
*             4=costa rural, 5=sierra rural, 6=selva rural, 7=Lima Metro)
eststo costa: reghdfe log_ingreso did `controles' if inlist(dominio,1,4), ///
    absorb(anio conglome) vce(cluster conglome)
eststo sierra: reghdfe log_ingreso did `controles' if inlist(dominio,2,5), ///
    absorb(anio conglome) vce(cluster conglome)
eststo selva: reghdfe log_ingreso did `controles' if inlist(dominio,3,6), ///
    absorb(anio conglome) vce(cluster conglome)

esttab hom muj costa sierra selva using "$tabs\heterogeneity.tex", ///
    replace label booktabs ///
    title("Heterogeneidad del efecto de Ley 31110") ///
    mtitles("Hombres" "Mujeres" "Costa" "Sierra" "Selva") ///
    keep(did) b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N, fmt(0) labels("Observaciones"))

/*---------------------------------------------------------------------------
  4. MARGEN EXTENSIVO
---------------------------------------------------------------------------*/
* Efecto sobre probabilidad de trabajar en sector agrícola
* (requiere datos de toda la muestra, no solo los dos grupos)
* Ver 03_extensive_margin.do

display "Análisis completado. Revisar figuras en $figs y tablas en $tabs"
