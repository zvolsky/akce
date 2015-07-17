# -*- coding: utf-8 -*-

from mzw2p import Q
from plugin_ckeditor import CKEditor

ckeditor = CKEditor(db)
# ckeditor.define_tables()  -- done in controllers

db.define_table('typ_zacatku',
        Field('typ', length=48),
        format='%(typ)s'
        )

db.define_table('typ_kontaktu',
        Field('typ', length=96, label=Q('Typ kontaktu')),
        Field('lze_pouzivat', 'boolean', label=Q('lze použít')),  # existuje podpora zasílání pozvánek na tento typ kontaktu
        format='%(typ)s'
        )

db.define_table('typ_mista',
        Field('typ', length=96),
        format='%(typ)s'
        )

db.define_table('misto',
        Field('idtyp_mista', db.typ_mista),
        Field('misto', length=128),
        Field('lat', 'decimal(10,5)'),
        Field('lon', 'decimal(10,5)'),
        format='%(misto)s'
        )

db.define_table('typ_odkaz',
        Field('typ', length=96),
        format='%(typ)s'
        )

db.define_table('typ_upload',
        Field('typ', length=96),
        format='%(typ)s'
        )

db.define_table('typ_ucasti',
        Field('typ', length=48),
        Field('muj_status', length=48),
        format='%(typ)s'
        )

#--------------------------------

db.define_table('prijemce',
        Field('idauth_user', db.auth_user, readable=False, writable=False, default=auth.user_id),
        Field('nick', length=96),
        Field('poznamka', 'text'),
        format='%(nick)s'
        )

db.define_table('kontakt',
        Field('idauth_user', db.auth_user, readable=False, writable=False, default=auth.user_id),
        Field('idprijemce', db.prijemce),
        Field('idtyp_kontaktu', db.typ_kontaktu, label=Q('Typ kontaktu')),
        Field('upresneni_typu', length=96, label=Q('Upřesnění typu (např. pevná, do práce, jen v prac.dny,..)')),
        Field('kontakt', length=96),
        Field('lze_pouzit', 'boolean', default=True, label=Q('lze použít')),      # zasílat pozvánky na tento kontakt, pokud pro daný typ existuje podpora
        format='%(kontakt)s'
        )

db.define_table('kategorie_akce',
        Field('idauth_user', db.auth_user, readable=False, writable=False, default=auth.user_id),
        Field('plati', 'boolean', default=True, writable=False),
        Field('kategorie', length=96),
        format='%(kategorie)s'
        )

db.define_table('akce',
        Field('idauth_user', db.auth_user, writable=False, default=auth.user_id),  # hlavní správce akce
        Field('idkategorie_akce', db.kategorie_akce),
        Field('plati', 'boolean', default=True, label=Q("platná")),
        Field('zrusena', 'datetime', writable=False),
        Field('nazev', length=256),
        Field('verejne_vsem', 'boolean', default=True, label=Q('zobrazovat veřejně')),
        Field('prihlasit_do', 'datetime', label=Q('Přihlásit do'), comment=Q('prosím, přihlaste se do ..')),
        Field('minimalne', 'integer', label=Q('Minimální počet'), comment=Q('jinak bude zrušeno po datu pro přihlášení')),
        Field('kapacita', 'integer', label=Q('Kapacita akce'), comment=Q('maximální počet účastníků')),
        Field('hoste', 'integer', label=Q('Další účastníci'), comment=Q('účastníci navíc, mimo online přihlašování')),
        Field('zacatek', 'datetime'),
        Field('konec', 'datetime'),
        Field('opakovani', length=8), # empty | wNNNNNNN(týdně,N=den v týdnu 1=Po..7=Ne) | eN(ob týden) | 1N,2N,3N,4N,lN (1-4|poslední N v měsíci)
        Field('opakovat_do', 'datetime'),
        Field('popis', 'text', widget=ckeditor.widget),
        Field('priprava_poznamky', 'text', widget=ckeditor.widget),
        Field('zapis_verejny', 'text', widget=ckeditor.widget),
        Field('zapis_soukrome', 'text', widget=ckeditor.widget),
        format='%(nazev)s'
        )

db.define_table('planovani_akce',
        Field('idakce', db.akce, writable=False),
        Field('od_roku', 'integer'),
        Field('do_roku', 'integer'),
        Field('od_mesice', 'integer'),
        Field('do_mesice', 'integer'),
        Field('plan_zacatek', 'string', length=128),
        Field('plan_konec', 'string', length=128),
        )

db.define_table('vyjimka_opakovani',
        Field('idakce', db.akce, writable=False),
        Field('dne', 'date'),
        Field('nahradni_zacatek', 'datetime'),
        Field('nahradni_konec', 'datetime'),
        format='%(dne)s'
        )

db.define_table('sablona_cen',
        Field('idauth_user', db.auth_user, readable=False, writable=False, default=auth.user_id),
        Field('podminky', length=256),
        format='%(podminky)s'
        )

db.define_table('cena_akce',
        Field('idakce', db.akce, writable=False),
        Field('do_dne', 'datetime'),
        Field('cena', 'decimal(8,2)'),
        Field('podminky', length=256),
        format='%(cena)s'
        )

db.define_table('zacatek_akce',
        Field('idakce', db.akce, writable=False),
        Field('idtyp_zacatku', db.typ_zacatku),
        Field('cas', 'datetime'),
        Field('misto', length=256),
        format='%(cas)s %s(misto)s'
        )

db.define_table('etapa',
        Field('idakce', db.akce, writable=False),
        Field('den', 'integer'),
        Field('planovana', 'boolean'),
        Field('realna', 'boolean'),
        Field('datum', 'datetime'),
        Field('nazev', length=256, label=Q('Název'), comment=Q('název nebo trasa')),
        Field('popis', 'text', widget=ckeditor.widget),
        Field('priprava_poznamky', 'text', widget=ckeditor.widget),
        Field('zapis_verejny', 'text', widget=ckeditor.widget),
        Field('zapis_soukrome', 'text', widget=ckeditor.widget),
        format='%(den)s'
        )

db.define_table('misto_akce',
        Field('idakce', db.akce, writable=False),
        Field('idetapa_plan', db.etapa, writable=False),
        Field('idetapa_real', db.etapa, writable=False),
        Field('idmisto', db.misto),
        Field('misto', length=256),
        Field('plan_cas', 'datetime'),
        Field('plan_cas_do', 'datetime'),
        Field('plan_km', 'decimal(9,3)'),
        Field('cas', 'datetime'),
        Field('cas_do', 'datetime'),
        Field('km', 'decimal(9,3)'),
        Field('popis_verejny', 'text'),
        Field('popis_soukromy', 'text'),
        format='%(misto)s'
        )

db.define_table('odkaz_akce',
        Field('idakce', db.akce, writable=False),
        Field('idetapa_plan', db.etapa),
        Field('idetapa_real', db.etapa),
        Field('idmisto_akce', db.misto_akce),
        Field('idmisto', db.misto),
        Field('idtyp_odkaz', db.typ_odkaz),
        Field('odkaz', 'text'),
        Field('popis_verejny', 'text'),
        Field('popis_soukromy', 'text'),
        )

db.define_table('upload_akce',
        Field('idakce', db.akce, writable=False),
        Field('idetapa_plan', db.etapa),
        Field('idetapa_real', db.etapa),
        Field('idmisto_akce', db.misto_akce),
        Field('idmisto', db.misto),
        Field('idtyp_upload', db.typ_upload),
        Field('upload', length=256),
        Field('popis_verejny', 'text'),
        Field('popis_soukromy', 'text'),
        )

db.define_table('ucast',
        Field('idtyp_ucasti', db.typ_ucasti),
        Field('idakce', db.akce, writable=False),
        Field('idauth_user', db.auth_user),
        Field('plati', 'boolean'),
        Field('plati_od', 'datetime'),
        Field('platilo_do', 'datetime'),
        )

db.define_table('prijemci',
        Field('idauth_user', db.auth_user, readable=False, writable=False, default=auth.user_id),
        Field('idprijemce', db.prijemce),
        Field('skupina', length=128),
        format='%(skupina)s'
        )

db.define_table('informace',
        Field('idakce', db.akce, writable=False),
        Field('predmet', length=256),
        Field('obsah', 'text'),
        format='%(predmet)s'
        )

db.define_table('zaslani_skupine',
        Field('idinformace', db.informace, writable=False),
        Field('idtyp_ucasti', db.typ_ucasti),
        Field('idprijemci', db.prijemci),
        Field('idprijemce', db.prijemce),
        Field('lze_opakovane', 'boolean'),
        Field('cas', 'datetime'),
        Field('kolika', 'integer'),
        format='%(cas)s'
        )

db.define_table('protokol_mailu',
        Field('idzaslani_skupine', db.zaslani_skupine, writable=False),
        Field('idinformace', db.informace, writable=False),
        Field('idprijemce', db.prijemce, writable=False),       # if příjemce v kontaktech
        Field('idauth_user', db.auth_user, writable=False),     # if příjemce v sociální síti
        )

db.define_table('blokovane_kontakty',
        Field('idinformace', db.informace),                      # poštovní zásilka, která vyvolala blokaci
        Field('plati', 'boolean', default=True, writable=False),
        Field('blokovane', 'integer', writable=False),   # hash blokovaného mailu
        Field('blokovan_od', 'datetime', writable=False),
        Field('blokovan_do', 'datetime', writable=False),
        )

db.define_table('vyjimka_pozvanek',
        Field('idkontakt', db.kontakt),
        Field('idauth_user', db.auth_user),              # pro kterého odesílajícího autora
        Field('plati', 'boolean', default=True, writable=False),
        Field('povoleno', 'boolean', writable=False),    # True-povoleno, False-zakázáno
        Field('vyjimka_od', 'datetime', writable=False),
        Field('vyjimka_do', 'datetime', writable=False),
        format='%(povoleno)s %(od)s'
        )
