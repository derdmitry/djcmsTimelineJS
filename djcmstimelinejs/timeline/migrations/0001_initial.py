# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table(u'timeline_news', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('show_title', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'timeline', ['News'])

        # Adding model 'Asset'
        db.create_table(u'timeline_asset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('media', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('credit', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'timeline', ['Asset'])

        # Adding model 'Item'
        db.create_table(u'timeline_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('classname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timeline.Asset'])),
        ))
        db.send_create_signal(u'timeline', ['Item'])

        # Adding model 'Timeline'
        db.create_table(u'timeline_timeline', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'timeline', ['Timeline'])

        # Adding M2M table for field items on 'Timeline'
        m2m_table_name = db.shorten_name(u'timeline_timeline_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('timeline', models.ForeignKey(orm[u'timeline.timeline'], null=False)),
            ('item', models.ForeignKey(orm[u'timeline.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['timeline_id', 'item_id'])


    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table(u'timeline_news')

        # Deleting model 'Asset'
        db.delete_table(u'timeline_asset')

        # Deleting model 'Item'
        db.delete_table(u'timeline_item')

        # Deleting model 'Timeline'
        db.delete_table(u'timeline_timeline')

        # Removing M2M table for field items on 'Timeline'
        db.delete_table(db.shorten_name(u'timeline_timeline_items'))


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
        u'timeline.item': {
            'Meta': {'object_name': 'Item'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timeline.Asset']"}),
            'classname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'timeline.news': {
            'Meta': {'object_name': 'News', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'show_title': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'timeline.timeline': {
            'Meta': {'object_name': 'Timeline'},
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['timeline.Item']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['timeline']