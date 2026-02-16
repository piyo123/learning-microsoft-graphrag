import pandas as pd
import json
import html
from typing import Dict, List
from copy import deepcopy
from typing import Any

#############
# Helper:
#############
def get_document_name(document_id: int) -> str:
    df = pd.read_parquet("../output/documents.parquet")
    row = df[df["id"] == document_id].iloc[0]
    return row["title"]

def get_text_unit(text_unit_id: int) -> str:
    df = pd.read_parquet("../output/text_units.parquet")
    row = df.loc[df["id"] == text_unit_id].iloc[0]
    return row["text"]
    
def get_text_unit_with_document_name(text_unit_id: int) -> Dict:
    df = pd.read_parquet("../output/text_units.parquet")
    row = df.loc[df["id"] == text_unit_id].iloc[0]
    return {
        "document_name": get_document_name(row["document_id"]),
        "text": row["text"]
    }

# 表示用
def pretty_json_for_notebook(obj: Any) -> str:
    def _unescape(v):
        if isinstance(v, str):
            return html.unescape(v)
        elif isinstance(v, dict):
            return {k: _unescape(val) for k, val in v.items()}
        elif isinstance(v, list):
            return [_unescape(item) for item in v]
        else:
            return v

    clean = _unescape(deepcopy(obj))
    return json.dumps(clean, indent=2, ensure_ascii=False)



#############
# functions to get references:
#############
def get_source_references(text_unit_human_readable_id: int) -> Dict:
    df = pd.read_parquet("../output/text_units.parquet")
    row = df.loc[df["human_readable_id"] == text_unit_human_readable_id].iloc[0]

    return {
        "document_name": get_document_name(row["document_id"]),
        "text": row["text"]
    }

def get_entity_references(entity_human_readable_id: int) -> List[Dict]:
    df = pd.read_parquet("../output/entities.parquet")
    row = df.loc[df["human_readable_id"] == entity_human_readable_id].iloc[0]
    entity_name = row["title"]
    text_unit_ids = [str(s) for s in row["text_unit_ids"]]

    return [
        {
            "entity": entity_name,
            "document": get_text_unit_with_document_name(t).get("document_name", "N/A"),
            "text_unit_id": t,
            "text": get_text_unit(t)
        }
        for t in text_unit_ids
    ]

def get_relationship_references(relationship_human_readable_id: int) -> List[Dict]:
    df = pd.read_parquet("../output/relationships.parquet")
    row = df.loc[df["human_readable_id"] == relationship_human_readable_id].iloc[0]
    source = row["source"]
    target = row["target"]
    weight = row["weight"]
    text_unit_ids = [str(s) for s in row["text_unit_ids"]]

    return [
        {
            "relationship_source": source,
            "relationship_target": target,
            "weight": weight,
            "document": get_text_unit_with_document_name(t).get("document_name", "N/A"),
            "text_unit_id": t,
            "text": get_text_unit(t)
        }
        for t in text_unit_ids
    ]

def get_relationship_references_without_text_units(relationship_human_readable_id: int) -> Dict:
    df = pd.read_parquet("../output/relationships.parquet")
    row = df.loc[df["human_readable_id"] == relationship_human_readable_id].iloc[0]

    return  {
            "relationship_source": row["source"],
            "relationship_target": row["target"],
            "description": row["description"],
            "weight": row["weight"],
        }

def get_community_report_references(repot_human_readable_id: int) -> List[Dict]:
    df_r = pd.read_parquet("../output/community_reports.parquet")
    row_r = df_r.loc[df_r["human_readable_id"] == repot_human_readable_id].iloc[0]
    community_id = int(row_r["community"])
    community_report_title = row_r["title"]
    community_report_summary = row_r["summary"]
    df_c = pd.read_parquet("../output/communities.parquet")
    row_c = df_c.loc[df_c["community"] == community_id].iloc[0]

    text_unit_ids = [str(s) for s in row_c["text_unit_ids"]]

    return [
        {
            "community_network_name": community_report_title,
            "community_report_summary": community_report_summary,
            "document": get_text_unit_with_document_name(t).get("document_name", "N/A"),
            "text_unit_id": t,
            "text": get_text_unit(t)
        }
        for t in text_unit_ids
    ]

def get_community_report_references_without_text_units(repot_human_readable_id: int) -> Dict:
    df = pd.read_parquet("../output/community_reports.parquet")
    row = df.loc[df["human_readable_id"] == repot_human_readable_id].iloc[0]
    community_id = int(row["community"])
    community_report_title = row["title"]
    community_report_summary = row["summary"]
    
    return  {
            "community_network_name": community_report_title,
            "community_report_summary": community_report_summary,
        }

def get_network_by_name(network_name: int) -> List[Dict]:
    df = pd.read_parquet("../output/community_reports.parquet")
    rows = df[df["title"].str.contains(network_name, case=False, na=False, regex=False)]
    
    return [
        {
            "community_reports_id": r["id"],
            "community_network_name": r["title"],
            "community_report_summary": r["summary"],
        } for idx, r in rows.iterrows()
    ]