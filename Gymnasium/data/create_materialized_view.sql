-- Drop the materialized view if it exists
DROP MATERIALIZED VIEW IF EXISTS prelim_final_gymnasium;

-- Create the materialized view
CREATE MATERIALIZED VIEW prelim_final_gymnasium AS
WITH prelim_data AS (
    SELECT 
        g.år,
        g.kommun,
        g.skola,
        g.organistionsform,
        g.studievägskod,
        g.studieväg,
        g.antagningsgräns as antagningsgräns_prelim,
        g.median as median_prelim,
        g.antal_platser as antal_platser_prelim,
        g.antagna as antagna_prelim,
        g.reserver as reserver_prelim,
        g.lediga_platser as lediga_platser_prelim
    FROM gymnasium g
    WHERE g.är_preliminär = true
),
final_data AS (
    SELECT 
        g.år,
        g.skola,
        g.studievägskod,
        g.studieväg,
        g.antagningsgräns as antagningsgräns_final,
        g.median as median_final,
        g.antal_platser as antal_platser_final,
        g.antagna as antagna_final,
        g.reserver as reserver_final,
        g.lediga_platser as lediga_platser_final
    FROM gymnasium g
    WHERE g.är_preliminär = false
)
SELECT 
    p.år,
    p.kommun,
    p.skola,
    p.organistionsform,
    p.studievägskod,
    p.studieväg,
    p.antagningsgräns_prelim,
    f.antagningsgräns_final,
    p.median_prelim,
    f.median_final,
    p.antal_platser_prelim,
    f.antal_platser_final,
    p.antagna_prelim,
    f.antagna_final,
    p.reserver_prelim,
    f.reserver_final,
    p.lediga_platser_prelim,
    f.lediga_platser_final,
    (f.antagningsgräns_final - p.antagningsgräns_prelim) as grans_diff,
    (f.median_final - p.median_prelim) as median_diff
FROM prelim_data p
LEFT JOIN final_data f 
    ON p.år = f.år 
    AND p.skola = f.skola 
    AND p.studievägskod = f.studievägskod 
    AND p.studieväg = f.studieväg;

-- Create an index on the materialized view for better performance
CREATE INDEX idx_prelim_final_gymnasium_skola ON prelim_final_gymnasium(skola);
CREATE INDEX idx_prelim_final_gymnasium_studievag ON prelim_final_gymnasium(studieväg);
CREATE INDEX idx_prelim_final_gymnasium_ar ON prelim_final_gymnasium(år); 