from django.shortcuts import render
from django.http import HttpResponse
from .utils import generate_password

def index(request):
    # This will render our main HTML interface in Phase 4
    return render(request, 'generator/index.html')

def get_password(request):
    # Extract customisation parameters from the GET request
    try:
        length = int(request.GET.get('length', 16))
    except ValueError:
        length = 16
        
    include_upper = request.GET.get('uppercase') == 'true'
    include_lower = request.GET.get('lowercase') == 'true'
    include_numbers = request.GET.get('numbers') == 'true'
    include_symbols = request.GET.get('symbols') == 'true'
    exclude_ambiguous = request.GET.get('exclude_ambiguous') == 'true'

    # Safety fallback: if a user unchecks everything, default to all true to prevent errors
    if not any([include_upper, include_lower, include_numbers, include_symbols]):
        include_upper = include_lower = include_numbers = include_symbols = True

    try:
        password = generate_password(
            length=length,
            include_upper=include_upper,
            include_lower=include_lower,
            include_numbers=include_numbers,
            include_symbols=include_symbols,
            exclude_ambiguous=exclude_ambiguous
        )
        # Return only the password string for HTMX to inject into the page
        return HttpResponse(password)
    except ValueError as e:
        return HttpResponse(str(e), status=400)