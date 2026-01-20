@echo off
echo ========================================
echo  Aadhaar Analysis Pipeline - Full Run
echo ========================================
echo.

echo [1/3] Running Preprocessing Notebooks...
python utils/run_notebook.py notebooks/preprocessing/01_geographic_preprocessing.ipynb
python utils/run_notebook.py notebooks/preprocessing/02_age_demographics_preprocessing.ipynb
python utils/run_notebook.py notebooks/preprocessing/03_update_behavior_preprocessing.ipynb
python utils/run_notebook.py notebooks/preprocessing/04_anomaly_detection_preprocessing.ipynb
python utils/run_notebook.py notebooks/preprocessing/05_predictive_analytics_preprocessing.ipynb
python utils/run_notebook.py notebooks/preprocessing/06_pincode_analysis_preprocessing.ipynb

echo.
echo [2/3] Running Analysis Notebooks...
python utils/run_notebook.py notebooks/analysis/01_geographic_analysis.ipynb
python utils/run_notebook.py notebooks/analysis/02_age_demographics_analysis.ipynb
python utils/run_notebook.py notebooks/analysis/03_update_behavior_analysis.ipynb
python utils/run_notebook.py notebooks/analysis/04_anomaly_detection_analysis.ipynb
python utils/run_notebook.py notebooks/analysis/05_predictive_analytics_analysis.ipynb
python utils/run_notebook.py notebooks/analysis/06_pincode_analysis_analysis.ipynb
python utils/run_notebook.py notebooks/analysis/07_advanced_insights_analysis.ipynb
python utils/run_notebook.py notebooks/analysis/08_geographic_heatmaps.ipynb
python utils/run_notebook.py notebooks/analysis/09_population_ratio_heatmaps.ipynb

echo.
echo [3/3] Exporting Summaries...
python utils/batch_export_summaries.py

echo.
echo ========================================
echo  Pipeline Complete!
echo ========================================
echo Processed data: processed_data/
echo Visualizations: visualizations/
echo Summaries: analysis_results/
echo.
pause
