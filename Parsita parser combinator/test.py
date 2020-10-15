import pytest
from parser import *


def test_atom_1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a')
    monkeypatch.chdir(tmp_path)
    step('a', '--atom')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(ATOM (ID a))\n'


def test_atom_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('g (a)')
    monkeypatch.chdir(tmp_path)
    step('a', '--atom')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(ATOM (ID g) (ATOM (ID a)))\n'


def test_atom_3(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('g f h j')
    monkeypatch.chdir(tmp_path)
    step('a', '--atom')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(ATOM (ID g) (ATOM (ID f) (ATOM (ID h) (ATOM (ID j)))))\n'


def test_atom_4(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('g (a b) (cd f) s')
    monkeypatch.chdir(tmp_path)
    step('a', '--atom')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(ATOM (ID g) (ATOM (ID a) (ATOM (ID b))) (ATOM (ID cd)' \
                                        ' (ATOM (ID f))) (ATOM (ID s)))\n'


def test_atom_5(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('g (((((kek)))))')
    monkeypatch.chdir(tmp_path)
    step('a', '--atom')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(ATOM (ID g) (ATOM (ID kek)))\n'


def test_atom_list_1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('g [X] Y')
    monkeypatch.chdir(tmp_path)
    step('a', '--atom')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(ATOM (ID g) (cons (VAR X) nil) (VAR Y))\n'


def test_atom_list_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('[X] Y')
    monkeypatch.chdir(tmp_path)
    step('a', '--atom')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read().startswith('Expected')


def test_atom_var_1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('g (x X) (x Y) f')
    monkeypatch.chdir(tmp_path)
    step('a', '--atom')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(ATOM (ID g) (ATOM (ID x) (VAR X)) ' \
                                        '(ATOM (ID x) (VAR Y)) (ATOM (ID f)))\n'


def test_atom_var_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('g (X) (x Y)')
    monkeypatch.chdir(tmp_path)
    step('a', '--atom')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read().startswith('Expected')


def test_module_1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('module example.')
    monkeypatch.chdir(tmp_path)
    step('a', '--module')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(MODULE (ID example))\n'


def test_module_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('module .')
    monkeypatch.chdir(tmp_path)
    step('a', '--module')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read().startswith('Expected')


def test_module_3(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('module example')
    monkeypatch.chdir(tmp_path)
    step('a', '--module')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read().startswith('Expected')


def test_module_4(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('example.')
    monkeypatch.chdir(tmp_path)
    step('a', '--module')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read().startswith('Expected')


def test_module_5(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('modale example.')
    monkeypatch.chdir(tmp_path)
    step('a', '--module')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read().startswith('Expected')


def test_module_6(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('module Example.')
    monkeypatch.chdir(tmp_path)
    step('a', '--module')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read().startswith('Expected')


def test_typeexpr_1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a')
    monkeypatch.chdir(tmp_path)
    step('a', '--typeexpr')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(ATOM (ID a))\n'


def test_typeexpr_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('Y -> X')
    monkeypatch.chdir(tmp_path)
    step('a', '--typeexpr')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(TYPE (VAR Y) (VAR X))\n'


def test_typeexpr_3(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('(Y -> X)')
    monkeypatch.chdir(tmp_path)
    step('a', '--typeexpr')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(TYPE (VAR Y) (VAR X))\n'


def test_typeexpr_4(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('(A -> B) -> C')
    monkeypatch.chdir(tmp_path)
    step('a', '--typeexpr')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(TYPE (TYPE (VAR A) (VAR B)) (VAR C))\n'


def test_typeexpr_5(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('A -> B -> C')
    monkeypatch.chdir(tmp_path)
    step('a', '--typeexpr')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(TYPE (VAR A) (TYPE (VAR B) (VAR C)))\n'


def test_type_1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('type a b.')
    monkeypatch.chdir(tmp_path)
    step('a', '--type')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(TYPE_DEF (ID a) (ATOM (ID b)))\n'


def test_type_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('type a b -> X.')
    monkeypatch.chdir(tmp_path)
    step('a', '--type')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(TYPE_DEF (ID a) (TYPE (ATOM (ID b)) (VAR X)))\n'


def test_type_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('type filter (A -> o) -> list a -> list a -> o.')
    monkeypatch.chdir(tmp_path)
    step('a', '--type')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(TYPE_DEF (ID filter) (TYPE (TYPE (VAR A) (ATOM (ID o)))' \
                                        ' (TYPE (ATOM (ID list) (ATOM (ID a)))' \
                                        ' (TYPE (ATOM (ID list) (ATOM (ID a))) (ATOM (ID o))))))\n'


def test_type_3(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('type a (((b))).')
    monkeypatch.chdir(tmp_path)
    step('a', '--type')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(TYPE_DEF (ID a) (ATOM (ID b)))\n'


def test_type_4(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('type d a -> (((b))).')
    monkeypatch.chdir(tmp_path)
    step('a', '--type')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(TYPE_DEF (ID d) (TYPE (ATOM (ID a)) (ATOM (ID b))))\n'


def test_equal_disj(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a, b; c')
    (tmp_path / 'b').write_text('(((a), (b)); (c))')
    monkeypatch.chdir(tmp_path)
    step('a', '--disj')
    step('b', '--disj')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == open('b.out', 'r').read()


def test_relation_1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a.')
    monkeypatch.chdir(tmp_path)
    step('a', '--relation')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(DEF (ATOM (ID a)))\n'


def test_relation_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a b.')
    monkeypatch.chdir(tmp_path)
    step('a', '--relation')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(DEF (ATOM (ID a) (ATOM (ID b))))\n'


def test_relation_3(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a:-a.')
    monkeypatch.chdir(tmp_path)
    step('a', '--relation')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(DEF (ATOM (ID a)) (ATOM (ID a)))\n'


def test_relation_4(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a :-a.')
    monkeypatch.chdir(tmp_path)
    step('a', '--relation')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(DEF (ATOM (ID a)) (ATOM (ID a)))\n'


def test_relation_5(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a:-a b.')
    monkeypatch.chdir(tmp_path)
    step('a', '--relation')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(DEF (ATOM (ID a)) (ATOM (ID a) (ATOM (ID b))))\n'


def test_relation_6(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a b:- (a b)  .')
    monkeypatch.chdir(tmp_path)
    step('a', '--relation')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(DEF (ATOM (ID a) (ATOM (ID b))) (ATOM (ID a) (ATOM (ID b))))\n'


def test_relation_7(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a b:- a;b,c.')
    (tmp_path / 'b').write_text('a b:- a;(b,c).')
    (tmp_path / 'c').write_text('a b:- (a;b),c.')
    monkeypatch.chdir(tmp_path)
    step('a', '--relation')
    step('b', '--relation')
    step('c', '--relation')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == open('b.out', 'r').read()
    assert open('a.out', 'r').read() != open('c.out', 'r').read()


def test_relation_8(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a b:- a;b;c.')
    monkeypatch.chdir(tmp_path)
    step('a', '--relation')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(DEF (ATOM (ID a) (ATOM (ID b))) ' \
                                        '(DISJ (ATOM (ID a)) (ATOM (ID b)) (ATOM (ID c))))\n'


def test_relation_9(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a b :- a,b,c.')
    monkeypatch.chdir(tmp_path)
    step('a', '--relation')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(DEF (ATOM (ID a) (ATOM (ID b)))' \
                                        ' (CONJ (ATOM (ID a)) (ATOM (ID b)) (ATOM (ID c))))\n'


def test_relation_10(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('a (b (c))  :- (a b) .')
    monkeypatch.chdir(tmp_path)
    step('a', '--relation')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(DEF (ATOM (ID a) (ATOM (ID b) (ATOM (ID c))))' \
                                        ' (ATOM (ID a) (ATOM (ID b))))\n'


def test_list_1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('[]')
    monkeypatch.chdir(tmp_path)
    step('a', '--list')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(nil)\n'


def test_list_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('[a]')
    monkeypatch.chdir(tmp_path)
    step('a', '--list')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(cons (ATOM (ID a)) nil)\n'


def test_list_3(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('[A,B]')
    monkeypatch.chdir(tmp_path)
    step('a', '--list')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(cons (VAR A) (cons (VAR B) nil))\n'


def test_list_4(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('[a (b c), B, C]')
    monkeypatch.chdir(tmp_path)
    step('a', '--list')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(cons (ATOM (ID a) (ATOM (ID b) (ATOM (ID c))))' \
                                        ' (cons (VAR B) (cons (VAR C) nil)))\n'


def test_list_5(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('[a | T]')
    monkeypatch.chdir(tmp_path)
    step('a', '--list')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(cons (ATOM (ID a)) (VAR T))\n'


def test_list_6(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('[ [a] | T ]')
    monkeypatch.chdir(tmp_path)
    step('a', '--list')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(cons (cons (ATOM (ID a)) nil) (VAR T))\n'


def test_list_7(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('[ [H | T], a ]')
    monkeypatch.chdir(tmp_path)
    step('a', '--list')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(cons (cons (VAR H) (VAR T)) (cons (ATOM (ID a)) nil))\n'


def test_list_8(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('[a | a]')
    monkeypatch.chdir(tmp_path)
    step('a', '--list')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read().startswith('Expected')


def test_list_9(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('[A,B,]')
    monkeypatch.chdir(tmp_path)
    step('a', '--list')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read().startswith('Expected')


def test_list_10(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('[A,B')
    monkeypatch.chdir(tmp_path)
    step('a', '--list')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read().startswith('Expected')


def test_list_11(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('][')
    monkeypatch.chdir(tmp_path)
    step('a', '--list')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read().startswith('Expected')


def test_program_1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('module example.\t\ntype kek lol -> pep.\t\t\t'
                                'type filter (A -> o) -> list a -> \nlist a -> o.'
                                'f :-\t g.\n'
                                'a b:- a,b,c.')
    monkeypatch.chdir(tmp_path)
    step('a', '--program')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == '(MODULE (ID example))\n' \
                                        '(TYPE_DEF (ID kek) (TYPE (ATOM (ID lol)) (ATOM (ID pep))))\n' \
                                        '(TYPE_DEF (ID filter) (TYPE (TYPE (VAR A) (ATOM (ID o)))' \
                                        ' (TYPE (ATOM (ID list) (ATOM (ID a))) (TYPE (ATOM (ID list) (ATOM (ID a)))' \
                                        ' (ATOM (ID o))))))\n(DEF (ATOM (ID f)) (ATOM (ID g)))\n' \
                                        '(DEF (ATOM (ID a) (ATOM (ID b))) (CONJ (ATOM (ID a)) (ATOM (ID b))' \
                                        ' (ATOM (ID c))))\n'
