from .reports import HandlersReport

SAMPLELOG = """
2025-03-26 12:21:05,000 ERROR django.request: Internal Server Error: /admin/dashboard/ [192.168.1.67] - OSError: No space left on device
2025-03-26 12:47:21,000 DEBUG django.db.backends: (0.33) SELECT * FROM 'dashboard' WHERE id = 67;
2025-03-26 12:19:07,000 INFO django.request: GET /admin/login/ 201 OK [192.168.1.86]
2025-03-26 12:01:43,000 WARNING django.security: DatabaseError: Deadlock detected
2025-03-26 12:00:06,000 CRITICAL django.core.management: IntegrityError: duplicate key value violates unique constraint
"""

def test_process_and_counts(tmp_path):
    logfile = tmp_path / "sample.log"
    logfile.write_text(SAMPLELOG.strip())

    rpt = HandlersReport()
    with open(logfile, "r", encoding="utf-8") as f:
        for line in f:
            rpt.process_line(line)

    # Проверим, что в ручках payments и orders подсчитано правильно
    data = rpt._counts
    assert data["/admin/login/"]["INFO"] == 1
    assert data["/admin/dashboard/"]["ERROR"] == 1
    # общее число запросов
    assert rpt._total == 2

def test_generate_output_contains_headers_and_totals(tmp_path):
    rpt = HandlersReport()
    # внесём пару строк вручную
    rpt._counts["/a/"]["DEBUG"] = 2
    rpt._counts["/a/"]["INFO"] = 3
    rpt._counts["/b/"]["ERROR"] = 1
    rpt._total = 6

    out = rpt.generate()
    # заголовок
    assert "Total requests: 6" in out
    assert "HANDLER" in out
    # проверим, что наши ручки упомянуты
    assert "/a/" in out
    assert "/b/" in out
    # и что суммарная строка есть
    assert out.strip().splitlines()[-1].strip().startswith(str(2))
