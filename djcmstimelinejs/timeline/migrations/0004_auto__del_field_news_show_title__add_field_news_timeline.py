# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'News.show_title'
        db.delete_column(u'timeline_news', 'show_title')

        # Adding field 'News.timeline'
        db.add_column(u'timeline_news', 'timeline',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timeline.Timeline'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'News.show_title'
        db.add_column(u'timeline_news', 'show_title',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Deleting field 'News.timeline'
        db.delete_column(u'timeline_news', 'timeline_id')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'timeline.asset': {
            'Meta': {'object_name': 'Asset'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'timeline.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'timeline.date': {
            'Meta': {'object_name': 'Date'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timeline.Asset']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timeline.Category']", 'null': 'True', 'blank': 'True'}),
            'classname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'endDate': ('django.db.models.fields.DateField', [], {}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'timeline.news': {
            'Meta': {'object_name': 'News', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timeline.Timeline']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'timeline.timeline': {
            'Meta': {'object_name': 'Timeline'},
            'date': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['timeline.Date']", 'symmetrical': 'False'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['timeline']