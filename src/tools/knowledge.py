import sqlite3
import json
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool

DB_PATH = "src/data/nodes.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@tool
def search_node_types(query: str) -> List[Dict[str, Any]]:
    """Search for n8n node types by name or description.
    
    Args:
        query: Search term (e.g., "slack", "webhook")
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT node_type, display_name, description 
            FROM nodes 
            WHERE node_type LIKE ? OR display_name LIKE ?
            LIMIT 10
        """
        cursor.execute(sql, (f'%{query}%', f'%{query}%'))
        results = []
        for row in cursor.fetchall():
            results.append({
                "name": row["node_type"],
                "displayName": row["display_name"],
                "description": row["description"]
            })
        conn.close()
        return results
    except Exception as e:
        return [{"error": str(e)}]

@tool
def get_node_schema(node_type: str) -> Dict[str, Any]:
    """Get the full JSON schema/definition for a specific node type.
    
    Args:
        node_type: The internal n8n name (e.g., "n8n-nodes-base.slack")
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT properties_schema FROM nodes WHERE node_type = ?"
        cursor.execute(sql, (node_type,))
        row = cursor.fetchone()
        conn.close()
        
        if row and row['properties_schema']:
            return json.loads(row['properties_schema'])
        return {"error": "Node not found or no schema available"}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_all_node_names() -> List[str]:
    """Get a list of all available node names in the knowledge base."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT node_type FROM nodes"
        cursor.execute(sql)
        results = [row['node_type'] for row in cursor.fetchall()]
        conn.close()
        return results
    except Exception as e:
        return [f"Error: {e}"]
