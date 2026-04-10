# v1-original-python: AUS Auto Service v1 (Original AI Pipeline)

This folder contains the original Python-based AUS Auto Service system (v1), which was the first implementation using:

- **AI/ML Pipeline**: ML models for material usage forecasting
- **Supabase Backend**: Cloud database integration
- **LINE Bot Integration**: Thai LINE messaging API for notifications
- **Metabase Visualization**: Data analytics and dashboards
- **Docker Support**: Containerized deployment

## Original Files

- `run_ai.py` - Run the AI/ML pipeline for forecasting
- `run_api.py` - Start the LINE Bot API server
- `run_etl.py` - Run ETL (Extract, Transform, Load) pipeline
- `reset_db.py` - Reset the Supabase database
- `docker-compose.yml` - Docker container orchestration
- `DockerFile` - Docker image definition
- `src_old_api/` - Original API module for LINE Bot
- `src_old_core/` - Original core config and database modules
- `src_old_nlp/` - Original NLP engine module
- `src_old_workers/` - Original background worker modules
- `note/` - Development notes and documentation

## Status

**Archived** - This version is no longer maintained. See Phase 2 (Streamlit) for active development.

## Tags

- `v1.0.0-original` - Original AI pipeline release
- `v1.5.0-vba` - Added Excel VBA system

## Next Version

See **Phase 2: Streamlit Implementation** in the root README.

## To Restore

To check out the original v1 pipeline code:

```bash
git checkout v1.0.0-original
```

This will restore the complete state of the original system as it was before the migration to Streamlit.
