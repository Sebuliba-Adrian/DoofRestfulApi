from app.models import CategoryModel

def search_categories(q):
    '''
    method that gets data based on the search query provided
    '''
    categories = CategoryModel.query.filter(CategoryModel.name.contains(q)).all()
    return categories