# -*- coding: utf-8 -*-

@auth.requires_membership('admin')
def starts():
    grid = SQLFORM.grid(db.typ_zacatku,
                        showbuttontext=False)
    return dict(grid=grid)

@auth.requires_membership('admin')
def contacts():
    grid = SQLFORM.grid(db.typ_kontaktu,
                        showbuttontext=False)
    return dict(grid=grid)

@auth.requires_membership('admin')
def places():
    grid = SQLFORM.grid(db.typ_mista,
                        showbuttontext=False)
    return dict(grid=grid)

@auth.requires_membership('admin')
def links():
    grid = SQLFORM.grid(db.typ_odkaz,
                        showbuttontext=False)
    return dict(grid=grid)

@auth.requires_membership('admin')
def uploads():
    grid = SQLFORM.grid(db.typ_upload,
                        showbuttontext=False)
    return dict(grid=grid)

@auth.requires_membership('admin')
def partitipations():
    grid = SQLFORM.grid(db.typ_ucasti,
                        showbuttontext=False)
    return dict(grid=grid)
