qdrant:
	docker run -p 6333:6333 \
    	-v $(pwd)/qdrant_storage:/qdrant/storage:z \
    	qdrant/qdrant


app:
	poetry run streamlit run app.py