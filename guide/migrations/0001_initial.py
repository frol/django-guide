# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Guide'
        db.create_table('guide_guide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('html_selector', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('guide_text', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('vertical_position', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('horizontal_position', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tip_mode', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('visibility_mode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('guide', ['Guide'])

        # Adding model 'UserGuide'
        db.create_table('guide_userguide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='saw_guide_list', to=orm['auth.User'])),
            ('guide', self.gf('django.db.models.fields.related.ForeignKey')(related_name='saw_user_list', to=orm['guide.Guide'])),
            ('views_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal('guide', ['UserGuide'])


    def backwards(self, orm):
        
        # Deleting model 'Guide'
        db.delete_table('guide_guide')

        # Deleting model 'UserGuide'
        db.delete_table('guide_userguide')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'guide.guide': {
            'Meta': {'object_name': 'Guide'},
            'guide_text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'horizontal_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'html_selector': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tip_mode': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vertical_position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'visibility_mode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'who_saw': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'guide_list'", 'blank': 'True', 'through': "orm['guide.UserGuide']", 'to': "orm['auth.User']"})
        },
        'guide.userguide': {
            'Meta': {'object_name': 'UserGuide'},
            'guide': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'saw_user_list'", 'to': "orm['guide.Guide']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'saw_guide_list'", 'to': "orm['auth.User']"}),
            'views_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['guide']
