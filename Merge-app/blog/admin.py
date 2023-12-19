from django.contrib import admin
from django.http import HttpResponse
from .models import *
import csv, datetime

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_date', 'category', 'preview_image']
    search_fields = ['title', 'author__username']
    list_filter = ['author', 'category', 'tags', 'published_date']
    prepopulated_fields = {'slug': ('title',)}
    
class CommentAdmin(admin.ModelAdmin):
    list_filter = ['created']

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' 'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.name for field in fields])
    
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'

class UserAdmin(admin.ModelAdmin):
    
    actions = [export_to_csv] 
    search_fields = ['username', 'city']
    list_filter = ['city', 'country']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(Category)