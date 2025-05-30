class Query:
    @staticmethod
    def get_accords_query():
        return """
        SELECT
            a.name AS accord_name,
            a.background AS color,
            ROUND(SUM(pa.score), 2) AS accord_score
        FROM PerfumeAccords pa
        JOIN Accords a ON pa.accord_id = a.id
        GROUP BY a.id, a.name, a.background
        ORDER BY accord_score DESC
        """

    @staticmethod
    def get_notes_query():
        return """
        SELECT
            n.name AS note_name,
            ROUND(SUM(pn.score), 2) AS note_score
        FROM PerfumeNotes pn
        JOIN Notes n ON pn.note_id = n.id
        GROUP BY n.id, n.name
        ORDER BY note_score DESC
        """