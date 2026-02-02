import io
import json
import pandas as pd
from django.conf import settings
from .models import UploadedDataset

MAX_HISTORY = 5
EXPECTED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']


def parse_csv(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    col_map = {
        'Equipment Name': ['Equipment Name', 'EquipmentName', 'equipment_name', 'Name'],
        'Type': ['Type', 'type', 'Equipment Type'],
        'Flowrate': ['Flowrate', 'Flow rate', 'flowrate', 'Flow'],
        'Pressure': ['Pressure', 'pressure'],
        'Temperature': ['Temperature', 'temperature', 'Temp'],
    }
    rename = {}
    for standard, variants in col_map.items():
        for v in variants:
            if v in df.columns and standard not in rename.values():
                rename[v] = standard
                break
    if rename:
        df = df.rename(columns=rename)
    return df


def compute_summary(df: pd.DataFrame) -> dict:
    numeric_cols = ['Flowrate', 'Pressure', 'Temperature']
    numeric_cols = [c for c in numeric_cols if c in df.columns]
    averages = df[numeric_cols].mean().round(2).to_dict() if numeric_cols else {}
    type_dist = df['Type'].value_counts().to_dict() if 'Type' in df.columns else {}
    return {
        'total_count': len(df),
        'averages': averages,
        'type_distribution': type_dist,
    }


def ensure_history_limit():
    ids_to_keep = list(
        UploadedDataset.objects.order_by('-uploaded_at').values_list('id', flat=True)[:MAX_HISTORY]
    )
    UploadedDataset.objects.exclude(id__in=ids_to_keep).delete()


def create_dataset_from_df(df: pd.DataFrame, name: str) -> UploadedDataset:
    summary = compute_summary(df)
    raw_list = df.fillna('').to_dict(orient='records')
    for row in raw_list:
        for k, v in row.items():
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                row[k] = round(v, 2) if isinstance(v, float) else v
    obj = UploadedDataset.objects.create(
        name=name,
        row_count=len(df),
        summary_json=json.dumps(summary),
        raw_data_json=json.dumps(raw_list),
    )
    ensure_history_limit()
    return obj
