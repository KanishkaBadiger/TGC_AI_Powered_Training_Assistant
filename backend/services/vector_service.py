"""
Vector Service using ChromaDB for semantic search and embeddings
"""
import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any

# Initialize ChromaDB client
db_path = os.path.join(os.path.dirname(__file__), "..", "..", "database", "chroma")
os.makedirs(db_path, exist_ok=True)

client = chromadb.PersistentClient(path=db_path)

class VectorService:
    """Service for managing vectors and semantic search using ChromaDB"""
    
    @staticmethod
    def create_collection(collection_name: str) -> Any:
        """Create a new collection in ChromaDB"""
        try:
            collection = client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            return collection
        except Exception as e:
            print(f"Error creating collection: {e}")
            return None
    
    @staticmethod
    def add_resume_embeddings(user_id: int, resume_text: str) -> bool:
        """
        Add resume text to vector database for similarity search
        
        Args:
            user_id: User ID
            resume_text: Resume content
        
        Returns:
            Success status
        """
        try:
            collection = VectorService.create_collection("resumes")
            
            # Split resume into chunks for better embeddings
            chunks = resume_text.split("\n\n")
            
            for idx, chunk in enumerate(chunks):
                if chunk.strip():
                    collection.add(
                        ids=[f"user_{user_id}_chunk_{idx}"],
                        metadatas=[{"user_id": user_id, "chunk_index": idx}],
                        documents=[chunk]
                    )
            
            return True
        except Exception as e:
            print(f"Error adding resume embeddings: {e}")
            return False
    
    @staticmethod
    def search_similar_resumes(query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar resumes based on skills or experience
        
        Args:
            query: Search query (skill, technology, etc.)
            n_results: Number of results to return
        
        Returns:
            List of similar resume chunks with metadata
        """
        try:
            collection = VectorService.create_collection("resumes")
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            formatted_results = []
            if results and results['ids']:
                for i, id_ in enumerate(results['ids'][0]):
                    formatted_results.append({
                        "id": id_,
                        "document": results['documents'][0][i] if results['documents'] else "",
                        "distance": results['distances'][0][i] if results['distances'] else 0,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {}
                    })
            
            return formatted_results
        except Exception as e:
            print(f"Error searching resumes: {e}")
            return []
    
    @staticmethod
    def add_job_embeddings(job_id: str, job_description: str, skills: str) -> bool:
        """
        Add job posting to vector database
        
        Args:
            job_id: Job posting ID
            job_description: Job description text
            skills: Required skills
        
        Returns:
            Success status
        """
        try:
            collection = VectorService.create_collection("jobs")
            
            full_text = f"{job_description}\n\nRequired Skills: {skills}"
            
            collection.add(
                ids=[f"job_{job_id}"],
                metadatas=[{"job_id": job_id}],
                documents=[full_text]
            )
            
            return True
        except Exception as e:
            print(f"Error adding job embeddings: {e}")
            return False
    
    @staticmethod
    def find_matching_jobs(user_skills: str, n_results: int = 10) -> List[Dict[str, Any]]:
        """
        Find jobs matching user skills
        
        Args:
            user_skills: User's skills as string
            n_results: Number of results
        
        Returns:
            List of matching jobs
        """
        try:
            collection = VectorService.create_collection("jobs")
            results = collection.query(
                query_texts=[user_skills],
                n_results=n_results
            )
            
            formatted_results = []
            if results and results['ids']:
                for i, id_ in enumerate(results['ids'][0]):
                    formatted_results.append({
                        "job_id": id_,
                        "description": results['documents'][0][i] if results['documents'] else "",
                        "match_score": 1 - (results['distances'][0][i] if results['distances'] else 1),
                    })
            
            return formatted_results
        except Exception as e:
            print(f"Error finding matching jobs: {e}")
            return []
    
    @staticmethod
    def add_learning_resources(resource_id: str, content: str, topic: str) -> bool:
        """
        Add learning resources to vector database
        
        Args:
            resource_id: Resource unique ID
            content: Resource content
            topic: Topic covered
        
        Returns:
            Success status
        """
        try:
            collection = VectorService.create_collection("learning_resources")
            
            collection.add(
                ids=[f"resource_{resource_id}"],
                metadatas=[{"topic": topic}],
                documents=[content]
            )
            
            return True
        except Exception as e:
            print(f"Error adding learning resources: {e}")
            return False
    
    @staticmethod
    def search_learning_resources(query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant learning resources
        
        Args:
            query: Search query
            n_results: Number of results
        
        Returns:
            List of relevant resources
        """
        try:
            collection = VectorService.create_collection("learning_resources")
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            formatted_results = []
            if results and results['ids']:
                for i, id_ in enumerate(results['ids'][0]):
                    formatted_results.append({
                        "id": id_,
                        "content": results['documents'][0][i] if results['documents'] else "",
                        "relevance_score": 1 - (results['distances'][0][i] if results['distances'] else 1),
                    })
            
            return formatted_results
        except Exception as e:
            print(f"Error searching learning resources: {e}")
            return []
