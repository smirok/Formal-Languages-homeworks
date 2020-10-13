import pytest

import parser


def test_integrate_false_example_1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'Syntax error at EOF'


def test_integrate_false_example_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text(':- f.')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'Syntax error at :- by type CORKSCREW\nParser position : line:1, col:0'


def test_integrate_false_example_3(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f :- .')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'Syntax error at . by type DOT\nParser position : line:1, col:5'


def test_integrate_false_example_4(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f :- g; h, .')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'Syntax error at . by type DOT\nParser position : line:1, col:11'


def test_integrate_false_example_5(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f :- (g; (f).')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'Syntax error at . by type DOT\nParser position : line:1, col:12'


def test_integrate_false_example_6(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f () .')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'Syntax error at ) by type CLOSE_BRACKET\nParser position : line:1, col:3'


def test_integrate_empty_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == ''


def test_integrate_true_example_1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f.')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'DEFINITION\n--ATOM\n----ID f\n--.\n'


def test_integrate_true_example_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f      :-    g.')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'DEFINITION\n--ATOM\n----ID f\n--:-\n--DISJ' \
                                        '\n----CONJ\n------EXPRESSION\n--------ATOM\n----------ID g\n--.\n'


def test_integrate_true_example_3(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f :- g, h; t.')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'DEFINITION\n--ATOM\n----ID f\n--:-\n--DISJ\n' \
                                        '----CONJ\n------EXPRESSION\n--------ATOM\n' \
                                        '----------ID g\n------CONJ\n--------EXPRESSION\n' \
                                        '----------ATOM\n------------ID h\n----DISJ\n------CONJ\n' \
                                        '--------EXPRESSION\n----------ATOM\n------------ID t\n--.\n'


def test_integrate_true_example_4(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f :- g, (h; t).')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'DEFINITION\n--ATOM\n----ID f\n--:-\n--DISJ\n----CONJ\n' \
                                        '------EXPRESSION\n--------ATOM\n----------ID g\n------CONJ\n' \
                                        '--------EXPRESSION\n----------OBR\n----------DISJ\n' \
                                        '------------CONJ\n--------------EXPRESSION\n----------------ATOM\n' \
                                        '------------------ID h\n------------DISJ\n--------------CONJ\n' \
                                        '----------------EXPRESSION\n------------------ATOM\n' \
                                        '--------------------ID t\n----------CBR\n--.\n'


def test_integrate_true_example_5(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f a :- g, h (t c d).')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'DEFINITION\n--ATOM\n----ID f\n----ATOM\n------ID a\n' \
                                        '--:-\n--DISJ\n----CONJ\n------EXPRESSION\n--------ATOM\n' \
                                        '----------ID g\n------CONJ\n--------EXPRESSION\n----------ATOM\n' \
                                        '------------ID h\n------------OBR\n------------ATOM\n' \
                                        '--------------ID t\n--------------ATOM\n----------------ID c\n' \
                                        '----------------ATOM\n------------------ID d\n------------CBR\n--.\n'


def test_integrate_true_example_6(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f (cons h t) :- g h, f t.')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'DEFINITION\n--ATOM\n----ID f\n----OBR\n----ATOM\n' \
                                        '------ID cons\n------ATOM\n--------ID h\n--------ATOM\n' \
                                        '----------ID t\n----CBR\n--:-\n--DISJ\n----CONJ\n' \
                                        '------EXPRESSION\n--------ATOM\n----------ID g\n' \
                                        '----------ATOM\n------------ID h\n------CONJ\n' \
                                        '--------EXPRESSION\n----------ATOM\n------------ID f\n' \
                                        '------------ATOM\n--------------ID t\n--.\n'


def test_integrate_true_multibrackets(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f :- (((g))).')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'DEFINITION\n--ATOM\n----ID f\n--:-\n--DISJ\n----CONJ\n' \
                                        '------EXPRESSION\n--------OBR\n--------DISJ\n----------CONJ\n' \
                                        '------------EXPRESSION\n--------------OBR\n--------------DISJ\n' \
                                        '----------------CONJ\n------------------EXPRESSION\n' \
                                        '--------------------OBR\n--------------------DISJ\n' \
                                        '----------------------CONJ\n------------------------EXPRESSION\n' \
                                        '--------------------------ATOM\n----------------------------ID g\n' \
                                        '--------------------CBR\n--------------CBR\n--------CBR\n--.\n'


def test_integrate_true_multilines_and_empty_str(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('f\n:-\n\n\ng,h,g .')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'DEFINITION\n--ATOM\n----ID f\n--:-\n--DISJ\n' \
                                        '----CONJ\n------EXPRESSION\n--------ATOM\n' \
                                        '----------ID g\n------CONJ\n--------EXPRESSION\n' \
                                        '----------ATOM\n------------ID h\n--------CONJ\n' \
                                        '----------EXPRESSION\n------------ATOM\n--------------ID g\n--.\n'


def test_integrate_true_so_hard(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a').write_text('odd (cons H (cons H1 T)) (cons H T1) :- odd T T1.\n'
                                'odd (cons H nil) nil.\n'
                                'odd nil nil.')
    monkeypatch.chdir(tmp_path)
    parser.step('a')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert open('a.out', 'r').read() == 'DEFINITION\n--ATOM\n----ID odd\n----OBR\n----ATOM\n------ID cons\n' \
                                        '------ATOM\n--------ID H\n--------OBR\n--------ATOM\n----------ID cons\n' \
                                        '----------ATOM\n------------ID H1\n------------ATOM\n--------------ID T\n' \
                                        '--------CBR\n----CBR\n----ATOM\n------OBR\n------ATOM\n--------ID cons\n' \
                                        '--------ATOM\n----------ID H\n----------ATOM\n------------ID T1\n' \
                                        '------CBR\n--:-\n--DISJ\n----CONJ\n------EXPRESSION\n--------ATOM\n' \
                                        '----------ID odd\n----------ATOM\n------------ID T\n------------ATOM\n' \
                                        '--------------ID T1\n--.\nDEFINITION\n--ATOM\n----ID odd\n----OBR\n' \
                                        '----ATOM\n------ID cons\n------ATOM\n--------ID H\n--------ATOM\n' \
                                        '----------ID nil\n----CBR\n----ATOM\n------ID nil\n--.\nDEFINITION\n' \
                                        '--ATOM\n----ID odd\n----ATOM\n------ID nil\n------ATOM\n--------ID nil\n--.\n'
