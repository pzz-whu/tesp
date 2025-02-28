#!/bin/bash
# Copyright (C) 2017-2022 Battelle Memorial Institute
# file: run_market.sh

#(export FNCS_BROKER="tcp://*:5570" && export FNCS_LOG_LEVEL="DEBUG2" && FNCS_TRACE=yes && FNCS_LOG_STDOUT=yes && exec fncs_broker 20 &> broker.log &)
(export FNCS_BROKER="tcp://*:5570" && exec fncs_broker 20 &> broker.log &)
(export WEATHER_CONFIG=weatherIAH.json && export FNCS_FATAL=YES && export FNCS_LOG_STDOUT=yes && exec python3 -c "import tesp_support.api as tesp;tesp.startWeatherAgent('weatherIAH.dat')"  &> weatherIAH.log &)
(export WEATHER_CONFIG=weatherSPS.json && export FNCS_FATAL=YES && export FNCS_LOG_STDOUT=yes && exec python3 -c "import tesp_support.api as tesp;tesp.startWeatherAgent('weatherSPS.dat')"  &> weatherSPS.log &)
(export WEATHER_CONFIG=weatherELP.json && export FNCS_FATAL=YES && export FNCS_LOG_STDOUT=yes && exec python3 -c "import tesp_support.api as tesp;tesp.startWeatherAgent('weatherELP.dat')"  &> weatherELP.log &)
(export FNCS_FATAL=YES && exec gridlabd -D USE_FNCS -D METRICS_FILE=Bus1_metrics.json Bus1.glm &> Bus1.log &)
(export FNCS_FATAL=YES && exec gridlabd -D USE_FNCS -D METRICS_FILE=Bus2_metrics.json Bus2.glm &> Bus2.log &)
(export FNCS_FATAL=YES && exec gridlabd -D USE_FNCS -D METRICS_FILE=Bus3_metrics.json Bus3.glm &> Bus3.log &)
(export FNCS_FATAL=YES && exec gridlabd -D USE_FNCS -D METRICS_FILE=Bus4_metrics.json Bus4.glm &> Bus4.log &)
(export FNCS_FATAL=YES && exec gridlabd -D USE_FNCS -D METRICS_FILE=Bus5_metrics.json Bus5.glm &> Bus5.log &)
(export FNCS_FATAL=YES && exec gridlabd -D USE_FNCS -D METRICS_FILE=Bus6_metrics.json Bus6.glm &> Bus6.log &)
(export FNCS_FATAL=YES && exec gridlabd -D USE_FNCS -D METRICS_FILE=Bus7_metrics.json Bus7.glm &> Bus7.log &)
(export FNCS_FATAL=YES && exec gridlabd -D USE_FNCS -D METRICS_FILE=Bus8_metrics.json Bus8.glm &> Bus8.log &)
(export FNCS_CONFIG_FILE=Bus1_substation.yaml && export FNCS_FATAL=YES && exec python3 -c "import tesp_support.api as tesp;tesp.substation_loop('Bus1_agent_dict.json','Bus1', 72)" &> substation1.log &)
(export FNCS_CONFIG_FILE=Bus2_substation.yaml && export FNCS_FATAL=YES && exec python3 -c "import tesp_support.api as tesp;tesp.substation_loop('Bus2_agent_dict.json','Bus2', 72)" &> substation2.log &)
(export FNCS_CONFIG_FILE=Bus3_substation.yaml && export FNCS_FATAL=YES && exec python3 -c "import tesp_support.api as tesp;tesp.substation_loop('Bus3_agent_dict.json','Bus3', 72)" &> substation3.log &)
(export FNCS_CONFIG_FILE=Bus4_substation.yaml && export FNCS_FATAL=YES && exec python3 -c "import tesp_support.api as tesp;tesp.substation_loop('Bus4_agent_dict.json','Bus4', 72)" &> substation4.log &)
(export FNCS_CONFIG_FILE=Bus5_substation.yaml && export FNCS_FATAL=YES && exec python3 -c "import tesp_support.api as tesp;tesp.substation_loop('Bus5_agent_dict.json','Bus5', 72)" &> substation5.log &)
(export FNCS_CONFIG_FILE=Bus6_substation.yaml && export FNCS_FATAL=YES && exec python3 -c "import tesp_support.api as tesp;tesp.substation_loop('Bus6_agent_dict.json','Bus6', 72)" &> substation6.log &)
(export FNCS_CONFIG_FILE=Bus7_substation.yaml && export FNCS_FATAL=YES && exec python3 -c "import tesp_support.api as tesp;tesp.substation_loop('Bus7_agent_dict.json','Bus7', 72)" &> substation7.log &)
(export FNCS_CONFIG_FILE=Bus8_substation.yaml && export FNCS_FATAL=YES && exec python3 -c "import tesp_support.api as tesp;tesp.substation_loop('Bus8_agent_dict.json','Bus8', 72)" &> substation8.log &)
(export FNCS_CONFIG_FILE=tso8.yaml && export FNCS_FATAL=YES && exec python3 fncsTSO.py &> bulk.log &)
