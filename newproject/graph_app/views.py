import io
import csv
from django.shortcuts import render, redirect
from .models import GraphEdge, UploadedCSV
from .forms import CSVUploadForm
from django.http import JsonResponse
import pandas as pd
import logging
import json

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            if csv_file.name.endswith('.csv'):
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.reader(io_string, delimiter=',')
                
                # Create an entry for the uploaded CSV file
                uploaded_csv = UploadedCSV.objects.create(file_name=csv_file.name)

                added_records = 0  # Counter for added records
                for row in reader:
                    if len(row) >= 2:  # Ensure there are at least 2 elements
                        weight = row[2] if len(row) == 3 else None
                        try:
                            # Create the GraphEdge entry linked to the uploaded CSV
                            GraphEdge.objects.create(
                                node_from=row[0],
                                node_to=row[1],
                                weight=weight,
                                csv_file=uploaded_csv
                            )
                            added_records += 1
                        except Exception as e:
                            print(f"Error adding record {row}: {e}")  # Log the error
                
                # After uploading, redirect to visualize_data view
                # print("successfully uploaded ",csv_file.name,"to DATABASE" )
                return redirect('visualize_data')

            else:
                form.add_error('file', 'This is not a CSV file')

    return redirect('visualize_data')  # Redirect back to visualize if not POST


def visualize_data(request):
    uploaded_csvs = UploadedCSV.objects.order_by('-uploaded_at')[:5]
    graph_data = {}

    if request.method == 'POST':
        selected_csv_id = request.POST.get('csv_id')

        if 'visualize' in request.POST and selected_csv_id:
            edges = GraphEdge.objects.filter(csv_file_id=selected_csv_id)
            for edge in edges:
                graph_data[edge.id] = {
                    'from': edge.node_from,
                    'to': edge.node_to,
                    'weight': edge.weight
                }
            return JsonResponse({'graph_data': graph_data})

        elif 'delete' in request.POST and selected_csv_id:
            try:
                uploaded_csv = UploadedCSV.objects.get(id=selected_csv_id)
                # Delete related GraphEdge entries
                GraphEdge.objects.filter(csv_file=uploaded_csv).delete()
                # Then delete the uploaded CSV file
                uploaded_csv.delete()
                return JsonResponse({'success': True})
            except UploadedCSV.DoesNotExist:
                print(f"UploadedCSV with id {selected_csv_id} does not exist.")
            except Exception as e:
                print(f"An error occurred while deleting: {e}")
                return JsonResponse({'success': False})

    return render(request, 'visualize.html', {'graph_data': graph_data, 'uploaded_csvs': uploaded_csvs})

def get_recent_files(request):
    uploaded_csvs = UploadedCSV.objects.order_by('-uploaded_at')[:5]
    recent_files = [{
        'id': csv.id,
        'file_name': csv.file_name,
        'uploaded_at': csv.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
    } for csv in uploaded_csvs]
    
    return JsonResponse({'uploaded_csvs': recent_files})
