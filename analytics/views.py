from django.shortcuts import render
from .models import Sale
import csv
from io import TextIOWrapper

def home(request):
    sales = Sale.objects.all()
    total_sales = sum(s.amount for s in sales)
    categories = set(s.category for s in sales)
    return render(request, 'home.html', {'sales': sales, 'total': total_sales, 'categories': categories})

def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']

        # File type check
        if not csv_file.name.endswith('.csv'):
            return render(request, 'upload.html', {'error': 'Please upload a CSV file only.'})

        # Read CSV safely
        data = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.DictReader(data)

        # BOM / extra space / case correction
        fieldnames = [f.strip().replace('\ufeff', '') for f in reader.fieldnames]

        for row in reader:
            # Normalize keys (convert to lowercase, remove spaces)
            clean_row = {k.strip().lower(): v.strip() for k, v in row.items()}

            Sale.objects.create(
                date=clean_row.get('date'),
                product=clean_row.get('product'),
                category=clean_row.get('category'),
                amount=clean_row.get('amount'),
            )

        return render(request, 'upload.html', {'success': 'Data uploaded successfully! ✅'})

    return render(request, 'upload.html')
