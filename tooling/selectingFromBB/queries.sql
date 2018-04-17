select s.* from (select @experiment:="testinfected2017") unused, sessions_for_experiment s;


SELECT DISTINCT m.project_id
    FROM (select @experiment:="testinfected2017") unused, master_events m 
    INNER JOIN sessions_for_experiment s ON m.session_id=s.id 
    INNER JOIN sessions ses ON ses.id=m.session_id 
    AND project_id IS NOT NULL
    WHERE ses.created_at BETWEEN '2017-08-28 00:00:00' AND '2017-11-13 00:00:00'


    SELECT DISTINCT m.project_id, s.id AS session_id
                    FROM (select @experiment:="testinfected2017") unused, master_events m
                    INNER JOIN sessions_for_experiment s ON m.session_id=s.id
                    INNER JOIN sessions ses ON ses.id=m.session_id
                    AND project_id IS NOT NULL
                    WHERE ses.created_at BETWEEN 2017-08-28 00:00:00 AND 2017-11-13 00:00:00
                    
    ;

SELECT DISTINCT m.project_id
                    FROM (select @experiment:="testinfected2017") unused, master_events m
                    INNER JOIN sessions_for_experiment s ON m.session_id=s.id
                    INNER JOIN sessions ses ON ses.id=m.session_id
                    AND project_id IS NOT NULL
                    WHERE ses.created_at BETWEEN '2017-08-28 00:00:00' AND '2017-11-13 00:00:00';