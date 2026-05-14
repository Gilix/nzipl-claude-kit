# goodenough · Demo Queries

20 representative queries organized by use case. Each shows the question, the tools the bot would call, and a sketch of the answer.

## 1. Discovery (what does the data show?)

### Q1: "Which countries dominate solar panel manufacturing?"
**Tools**: query_pc_scores(tech="Solar", year=2024, top_n=10) + query_trade_flows(tech="Solar", product_type="Final Product", metric="value", top_n=10)
**Expected answer**: China dominates with >80% of polysilicon-to-module production. Vietnam and Malaysia are assembly hubs with high RCA but low PC (assembly without upstream depth). India and South Korea show strong PC trajectories with growing domestic capability.

### Q2: "What raw materials does Chile export for clean energy?"
**Tools**: query_trade_flows(exporter="CHL", tech="ALL", product_type="Raw Material", metric="value", year_start=2020, year_end=2024)
**Expected answer**: Lithium (HS 283691), copper cathodes (HS 740311), molybdenum (HS 261310). Chile is the #2 lithium exporter globally. Heavy upstream concentration with minimal midstream processing.

### Q3: "Show me the top 5 emerging competitors in wind turbine manufacturing"
**Tools**: query_pc_scores(tech="Wind", year=2024, min_score=0.3, max_rca=1, top_n=5, include_trend=true)
**Expected answer**: Countries with rising PC but RCA<1 -- building capability but not yet exporting their fair share. Likely includes India, Brazil, Turkey, Morocco, Mexico.

## 2. Comparison (how do countries stack up?)

### Q4: "Compare Mexico and Vietnam for battery supply chains"
**Tools**: compare_countries(countries=["MEX","VNM"], tech="Batteries", dimensions=["trade_value","rca_profile","pc_score","firms","value_chain_position"])
**Expected answer**: Vietnam leads in assembly (final product exports) but Mexico has deeper upstream (processed materials, components). PC scores diverge: Mexico's machinery cluster gives it process chain advantage.

### Q5: "How does India's solar capability compare to China's in 2024 vs 2015?"
**Tools**: query_pc_scores(tech="Solar", country="IND", include_trend=true) + query_pc_scores(tech="Solar", country="CHN", include_trend=true) + query_rca(country="IND", tech="Solar", year=2024) + query_rca(country="CHN", tech="Solar", year=2024)
**Expected answer**: China's PC has been >0.9 since 2010. India's rose from 0.4 to 0.7 (2015-2024) driven by electronics and chemicals clusters. India's RCA in polysilicon is still <0.3 (imports 90%+ from China).

### Q6: "Which African countries have the strongest clean energy manufacturing base?"
**Tools**: query_pc_scores(tech="ALL", year=2024, top_n=50) filtered to African countries + query_orbis_firms(tech="ALL", metric="by_country") filtered to Africa
**Expected answer**: South Africa leads across most technologies. Morocco has growing solar and wind. Egypt and Kenya show emerging signals in specific niches.

## 3. Value Chain Analysis (where are the bottlenecks?)

### Q7: "What's blocking Nigeria from solar manufacturing?"
**Tools**: query_rca(country="NGA", tech="Solar", year=2024) + query_pc_scores(tech="Solar", country="NGA") + query_pc_features(tech="Solar", top_n=10)
**Expected answer**: Nigeria's PC for Solar is very low (<0.15). Missing upstream capabilities: no glass processing (Industrial Materials cluster), minimal electronics (HS 85), no chemical processing for encapsulants. The bottleneck is the entire midstream, not a single product.

### Q8: "What upstream products predict competitiveness in batteries?"
**Tools**: query_pc_features(tech="Batteries", top_n=15, feature_type="hs_only")
**Expected answer**: Top SHAP features: lithium compounds (HS 283691), cobalt oxides (HS 282200), nickel matte (HS 750110), graphite (HS 250410), electrolyte chemicals. Process equipment (coating machines, mixing equipment) also highly predictive.

### Q9: "Which countries export process equipment for transmission but not transmission products?"
**Tools**: query_trade_flows(tech="Transmission", product_type="Process Equipment", metric="rca", year_start=2022, year_end=2024) cross-referenced with query_rca(tech="Transmission", product_type="Final Product")
**Expected answer**: Countries with RCA>1 in winding machines and insulation equipment but RCA<1 in transformers. These are capability suppliers that could vertically integrate.

## 4. Subnational (where in the country?)

### Q10: "Which Mexican states are best for EV component manufacturing?"
**Tools**: query_subnational(country="MEX", play="ev-components", metric="rca", admin_level="state") + query_subnational(country="MEX", play="ev-components", metric="relatedness") + query_subnational(country="MEX", play="ev-components", metric="parks", top_n=5)
**Expected answer**: Nuevo Leon leads in relatedness (0.577), Chihuahua in employment concentration. Top parks: those near 230kV+ substations with high clean energy share and existing automotive supply chain (Coahuila, Guanajuato).

### Q11: "What's Mexico's auto supplier RCA at the state level?"
**Tools**: query_subnational(country="MEX", play="auto-supplier", metric="rca", admin_level="state", top_n=10)
**Expected answer**: Coahuila (RCA 5.2), Chihuahua (4.8), Guanajuato (4.1) lead. These states concentrate >60% of Mexico's HS 8708 exports.

## 5. Methodology (what does this mean?)

### Q12: "What is predicted competitiveness and how is it different from RCA?"
**Tools**: explain_methodology(concept="predicted_competitiveness") + explain_methodology(concept="rca")
**Expected answer**: RCA is backward-looking (what does the country export today?). PC is forward-looking (given its upstream capabilities, could the country become competitive?). A country can have low RCA but high PC -- meaning it has the ingredients but hasn't assembled them yet.

### Q13: "How does the Green Dictionary work? What's in it?"
**Tools**: explain_methodology(concept="green_dictionary") + query_green_dict(technology="Solar") as example
**Expected answer**: A curated mapping of ~400 HS6 trade codes to 10 clean technologies. Each product is classified by type (Raw Material through Final Product) and stage (Upstream through Final). Built from industry knowledge, validated against IRENA and IEA product lists.

### Q14: "What are the five capability clusters?"
**Tools**: explain_methodology(concept="capability_clusters")
**Expected answer**: Electronics, Machinery, Mining & Metals, Industrial Materials, Chemicals. From WP4: these upstream clusters predict clean energy competitiveness. A country's profile across these five determines which technologies it can realistically pursue.

## 6. Strategic (what should we do?)

### Q15: "What's Brazil's best entry point into clean energy manufacturing?"
**Tools**: query_pc_scores(tech="ALL", country="BRA", year=2024) + query_rca(country="BRA", tech="ALL", year=2024, min_rca=1) + query_orbis_firms(country="BRA", tech="ALL")
**Expected answer**: Brazil has strong RCA in biofuel (established) and emerging capability in Wind (PC rising, growing RCA). Transmission is competitive (RCA>1 in transformers, strong metals cluster). Battery minerals (lithium, rare earths) are upstream but processing is minimal. Recommendation: Wind and Transmission leverage existing industrial base; Biofuel is mature. Battery processing is the ambitious bet.

### Q16: "We're advising the Indonesian government on industrial policy for clean energy. Where should they focus?"
**Tools**: query_pc_scores(tech="ALL", country="IDN") + query_rca(country="IDN", tech="ALL", year=2024) + query_pc_features for top-scoring tech + query_orbis_firms(country="IDN")
**Expected answer**: Multi-tool synthesis identifying Indonesia's strongest capabilities and gaps, grounded in PC scores and SHAP analysis.

### Q17: "Which countries could replace China as a source of polysilicon?"
**Tools**: query_trade_flows(tech="Solar", product_type="Processed Material", metric="value") filtered to polysilicon + query_rca for polysilicon HS codes + query_pc_scores(tech="Solar", min_score=0.3)
**Expected answer**: Germany, South Korea, Japan have small polysilicon capacity. India is scaling. But China's cost advantage (energy-intensive, coal-powered) is structural. Replacement requires either massive capital or acceptance of higher costs.

## 7. Cross-cutting

### Q18: "What are the most traded clean energy products globally?"
**Tools**: query_trade_flows(tech="ALL", metric="value", year_start=2024, year_end=2024, top_n=20)
**Expected answer**: Ranked list of top 20 clean energy products by global trade value. Likely dominated by lithium-ion batteries, solar cells, transformers, and wind turbine components.

### Q19: "How has the global clean energy trade landscape changed since 2010?"
**Tools**: query_trade_flows(tech="ALL", metric="value", year_start=2010, year_end=2010) + query_trade_flows(tech="ALL", metric="value", year_start=2024, year_end=2024) + query_pc_scores(tech="Solar", year=2010) vs 2024
**Expected answer**: Massive growth in Solar and Batteries trade. China's dominance increased. New players emerged (Vietnam, India, Morocco). Raw material trade shifted (lithium explosion post-2015).

### Q20: "Summarize the state of global battery competitiveness in 2024"
**Tools**: query_pc_scores(tech="Batteries", year=2024, top_n=15) + query_trade_flows(tech="Batteries", metric="value", top_n=10) + query_pc_features(tech="Batteries", top_n=10) + query_orbis_firms(tech="Batteries", metric="by_country")
**Expected answer**: Comprehensive synthesis of who leads, who's emerging, what drives competitiveness, where the firms are, and what the value chain looks like.
