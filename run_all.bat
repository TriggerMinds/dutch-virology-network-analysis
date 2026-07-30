pip install -r requirements.txt
python src/init_archive_db.py
python src/ingest_pdf_archive.py
python src/track_redaction_deltas.py
python src/fetch_open_macro_data.py
python src/fetch_open_academic_data.py
python src/sync_cordis_open_data.py
python src/verify_open_documents.py
python src/setup_multiplex_db.py
python src/build_coverage_dictionary.py
python src/setup_sql_views.py
python build_web_app.py
