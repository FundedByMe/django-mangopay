# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MangoPayUser'
        db.create_table(u'mangopay_mangopayuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mangopay_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_users', to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=99, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=99, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, null=True, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('country_of_residence', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('nationality', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
        ))
        db.send_create_signal(u'mangopay', ['MangoPayUser'])

        # Adding model 'MangoPayNaturalUser'
        db.create_table(u'mangopay_mangopaynaturaluser', (
            (u'mangopayuser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mangopay.MangoPayUser'], unique=True, primary_key=True)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('income_range', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'mangopay', ['MangoPayNaturalUser'])

        # Adding model 'MangoPayLegalUser'
        db.create_table(u'mangopay_mangopaylegaluser', (
            (u'mangopayuser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mangopay.MangoPayUser'], unique=True, primary_key=True)),
            ('business_name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('generic_business_email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('headquaters_address', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
        ))
        db.send_create_signal(u'mangopay', ['MangoPayLegalUser'])

        # Adding model 'MangoPayDocument'
        db.create_table(u'mangopay_mangopaydocument', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mangopay_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('mangopay_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_documents', to=orm['mangopay.MangoPayUser'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('refused_reason_message', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'mangopay', ['MangoPayDocument'])

        # Adding model 'MangoPayPage'
        db.create_table(u'mangopay_mangopaypage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_pages', to=orm['mangopay.MangoPayDocument'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'mangopay', ['MangoPayPage'])

        # Adding model 'MangoPayBankAccount'
        db.create_table(u'mangopay_mangopaybankaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mangopay_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_bank_accounts', to=orm['mangopay.MangoPayUser'])),
            ('mangopay_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('iban', self.gf('django_iban.fields.IBANField')(max_length=34)),
            ('bic', self.gf('django_iban.fields.SWIFTBICField')(max_length=11)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=254)),
        ))
        db.send_create_signal(u'mangopay', ['MangoPayBankAccount'])

        # Adding model 'MangoPayWallet'
        db.create_table(u'mangopay_mangopaywallet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mangopay_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('mangopay_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_wallets', to=orm['mangopay.MangoPayUser'])),
        ))
        db.send_create_signal(u'mangopay', ['MangoPayWallet'])

        # Adding model 'MangoPayPayOut'
        db.create_table(u'mangopay_mangopaypayout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mangopay_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('mangopay_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_payouts', to=orm['mangopay.MangoPayUser'])),
            ('mangopay_wallet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_payouts', to=orm['mangopay.MangoPayWallet'])),
            ('mangopay_bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_payouts', to=orm['mangopay.MangoPayBankAccount'])),
            ('execution_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=9, null=True, blank=True)),
            ('debited_funds', self.gf('money.contrib.django.models.fields.MoneyField')(default=0, no_currency_field=True, max_digits=12, decimal_places=2, blank=True)),
            ('fees', self.gf('money.contrib.django.models.fields.MoneyField')(default=0, no_currency_field=True, max_digits=12, decimal_places=2, blank=True)),
            ('debited_funds_currency', self.gf('money.contrib.django.models.fields.CurrencyField')(default='EUR', max_length=3)),
            ('fees_currency', self.gf('money.contrib.django.models.fields.CurrencyField')(default='EUR', max_length=3)),
        ))
        db.send_create_signal(u'mangopay', ['MangoPayPayOut'])

        # Adding model 'MangoPayCard'
        db.create_table(u'mangopay_mangopaycard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mangopay_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('expiration_date', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_valid', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'mangopay', ['MangoPayCard'])

        # Adding model 'MangoPayCardRegistration'
        db.create_table(u'mangopay_mangopaycardregistration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mangopay_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('mangopay_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_card_registrations', to=orm['mangopay.MangoPayUser'])),
            ('mangopay_card', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='mangopay_card_registration', unique=True, null=True, to=orm['mangopay.MangoPayCard'])),
        ))
        db.send_create_signal(u'mangopay', ['MangoPayCardRegistration'])

        # Adding model 'MangoPayPayIn'
        db.create_table(u'mangopay_mangopaypayin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mangopay_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('mangopay_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_payins', to=orm['mangopay.MangoPayUser'])),
            ('mangopay_wallet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_payins', to=orm['mangopay.MangoPayWallet'])),
            ('mangopay_card', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_payins', to=orm['mangopay.MangoPayCard'])),
            ('execution_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=9, null=True, blank=True)),
            ('result_code', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('secure_mode_redirect_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'mangopay', ['MangoPayPayIn'])

        # Adding model 'MangoPayRefund'
        db.create_table(u'mangopay_mangopayrefund', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mangopay_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('mangopay_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_refunds', to=orm['mangopay.MangoPayUser'])),
            ('mangopay_pay_in', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mangopay_refunds', to=orm['mangopay.MangoPayPayIn'])),
            ('execution_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=9, null=True, blank=True)),
            ('result_code', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
        ))
        db.send_create_signal(u'mangopay', ['MangoPayRefund'])


    def backwards(self, orm):
        # Deleting model 'MangoPayUser'
        db.delete_table(u'mangopay_mangopayuser')

        # Deleting model 'MangoPayNaturalUser'
        db.delete_table(u'mangopay_mangopaynaturaluser')

        # Deleting model 'MangoPayLegalUser'
        db.delete_table(u'mangopay_mangopaylegaluser')

        # Deleting model 'MangoPayDocument'
        db.delete_table(u'mangopay_mangopaydocument')

        # Deleting model 'MangoPayPage'
        db.delete_table(u'mangopay_mangopaypage')

        # Deleting model 'MangoPayBankAccount'
        db.delete_table(u'mangopay_mangopaybankaccount')

        # Deleting model 'MangoPayWallet'
        db.delete_table(u'mangopay_mangopaywallet')

        # Deleting model 'MangoPayPayOut'
        db.delete_table(u'mangopay_mangopaypayout')

        # Deleting model 'MangoPayCard'
        db.delete_table(u'mangopay_mangopaycard')

        # Deleting model 'MangoPayCardRegistration'
        db.delete_table(u'mangopay_mangopaycardregistration')

        # Deleting model 'MangoPayPayIn'
        db.delete_table(u'mangopay_mangopaypayin')

        # Deleting model 'MangoPayRefund'
        db.delete_table(u'mangopay_mangopayrefund')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mangopay.mangopaybankaccount': {
            'Meta': {'object_name': 'MangoPayBankAccount'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'bic': ('django_iban.fields.SWIFTBICField', [], {'max_length': '11'}),
            'iban': ('django_iban.fields.IBANField', [], {'max_length': '34'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mangopay_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mangopay_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_bank_accounts'", 'to': u"orm['mangopay.MangoPayUser']"})
        },
        u'mangopay.mangopaycard': {
            'Meta': {'object_name': 'MangoPayCard'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_valid': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'mangopay_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'mangopay.mangopaycardregistration': {
            'Meta': {'object_name': 'MangoPayCardRegistration'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mangopay_card': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'mangopay_card_registration'", 'unique': 'True', 'null': 'True', 'to': u"orm['mangopay.MangoPayCard']"}),
            'mangopay_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mangopay_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_card_registrations'", 'to': u"orm['mangopay.MangoPayUser']"})
        },
        u'mangopay.mangopaydocument': {
            'Meta': {'object_name': 'MangoPayDocument'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mangopay_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mangopay_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_documents'", 'to': u"orm['mangopay.MangoPayUser']"}),
            'refused_reason_message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'mangopay.mangopaylegaluser': {
            'Meta': {'object_name': 'MangoPayLegalUser', '_ormbases': [u'mangopay.MangoPayUser']},
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'generic_business_email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'headquaters_address': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'mangopayuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mangopay.MangoPayUser']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'mangopay.mangopaynaturaluser': {
            'Meta': {'object_name': 'MangoPayNaturalUser', '_ormbases': [u'mangopay.MangoPayUser']},
            'income_range': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'mangopayuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mangopay.MangoPayUser']", 'unique': 'True', 'primary_key': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'})
        },
        u'mangopay.mangopaypage': {
            'Meta': {'object_name': 'MangoPayPage'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_pages'", 'to': u"orm['mangopay.MangoPayDocument']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'mangopay.mangopaypayin': {
            'Meta': {'object_name': 'MangoPayPayIn'},
            'execution_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mangopay_card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_payins'", 'to': u"orm['mangopay.MangoPayCard']"}),
            'mangopay_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mangopay_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_payins'", 'to': u"orm['mangopay.MangoPayUser']"}),
            'mangopay_wallet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_payins'", 'to': u"orm['mangopay.MangoPayWallet']"}),
            'result_code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'secure_mode_redirect_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'})
        },
        u'mangopay.mangopaypayout': {
            'Meta': {'object_name': 'MangoPayPayOut'},
            'debited_funds': ('money.contrib.django.models.fields.MoneyField', [], {'default': '0', 'no_currency_field': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'debited_funds_currency': ('money.contrib.django.models.fields.CurrencyField', [], {'default': "'EUR'", 'max_length': '3'}),
            'execution_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fees': ('money.contrib.django.models.fields.MoneyField', [], {'default': '0', 'no_currency_field': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'fees_currency': ('money.contrib.django.models.fields.CurrencyField', [], {'default': "'EUR'", 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mangopay_bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_payouts'", 'to': u"orm['mangopay.MangoPayBankAccount']"}),
            'mangopay_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mangopay_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_payouts'", 'to': u"orm['mangopay.MangoPayUser']"}),
            'mangopay_wallet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_payouts'", 'to': u"orm['mangopay.MangoPayWallet']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'})
        },
        u'mangopay.mangopayrefund': {
            'Meta': {'object_name': 'MangoPayRefund'},
            'execution_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mangopay_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mangopay_pay_in': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_refunds'", 'to': u"orm['mangopay.MangoPayPayIn']"}),
            'mangopay_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_refunds'", 'to': u"orm['mangopay.MangoPayUser']"}),
            'result_code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'})
        },
        u'mangopay.mangopayuser': {
            'Meta': {'object_name': 'MangoPayUser'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'country_of_residence': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '99', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '99', 'null': 'True', 'blank': 'True'}),
            'mangopay_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nationality': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_users'", 'to': u"orm['auth.User']"})
        },
        u'mangopay.mangopaywallet': {
            'Meta': {'object_name': 'MangoPayWallet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mangopay_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mangopay_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mangopay_wallets'", 'to': u"orm['mangopay.MangoPayUser']"})
        }
    }

    complete_apps = ['mangopay']