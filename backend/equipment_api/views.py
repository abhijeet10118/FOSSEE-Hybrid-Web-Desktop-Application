from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from .models import UploadedDataset
from .serializers import UploadedDatasetSerializer
from .services import parse_csv, create_dataset_from_df


class UploadCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not file.name.lower().endswith('.csv'):
            return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            df = parse_csv(file)
        except Exception as e:
            return Response({'error': f'Invalid CSV: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        if df.empty:
            return Response({'error': 'CSV is empty'}, status=status.HTTP_400_BAD_REQUEST)
        name = file.name
        dataset = create_dataset_from_df(df, name)
        serializer = UploadedDatasetSerializer(dataset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        try:
            dataset = UploadedDataset.objects.get(pk=dataset_id)
        except UploadedDataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'id': dataset.id,
            'name': dataset.name,
            'uploaded_at': dataset.uploaded_at.isoformat(),
            'summary': dataset.summary,
            'row_count': dataset.row_count,
        })


class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        datasets = UploadedDataset.objects.all()[:5]
        serializer = UploadedDatasetSerializer(datasets, many=True)
        return Response(serializer.data)


class DatasetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        try:
            dataset = UploadedDataset.objects.get(pk=dataset_id)
        except UploadedDataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UploadedDatasetSerializer(dataset)
        return Response(serializer.data)


class PDFReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        try:
            dataset = UploadedDataset.objects.get(pk=dataset_id)
        except UploadedDataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=12
        )
        story = []
        story.append(Paragraph('Chemical Equipment Parameter Report', title_style))
        story.append(Paragraph(f'Dataset: {dataset.name}', styles['Normal']))
        story.append(Paragraph(f'Generated: {dataset.uploaded_at.strftime("%Y-%m-%d %H:%M")}', styles['Normal']))
        story.append(Spacer(1, 0.25*inch))
        summary = dataset.summary
        story.append(Paragraph('Summary', styles['Heading2']))
        story.append(Paragraph(f"Total equipment count: {summary.get('total_count', 0)}", styles['Normal']))
        av = summary.get('averages', {})
        if av:
            story.append(Paragraph(
                f"Averages — Flowrate: {av.get('Flowrate', 'N/A')}, Pressure: {av.get('Pressure', 'N/A')}, Temperature: {av.get('Temperature', 'N/A')}",
                styles['Normal']
            ))
        td = summary.get('type_distribution', {})
        if td:
            story.append(Paragraph('Type distribution: ' + ', '.join(f'{k}: {v}' for k, v in td.items()), styles['Normal']))
        story.append(Spacer(1, 0.25*inch))
        story.append(Paragraph('Data Table', styles['Heading2']))
        data = dataset.raw_data
        if data:
            headers = list(data[0].keys())
            table_data = [headers] + [[str(row.get(h, '')) for h in headers] for row in data]
            t = Table(table_data, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]))
            story.append(t)
        doc.build(story)
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{dataset.name}.pdf"'
        return response
