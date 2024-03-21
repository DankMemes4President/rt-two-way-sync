-- create function
CREATE or REPLACE FUNCTION push_change() RETURNS TRIGGER AS $$
    DECLARE
        payload json;
    BEGIN
        payload := row_to_json(new);
        PERFORM pg_notify('changes', json_build_array(tg_table_name, tg_op, payload)::text);
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

-- create trigger
CREATE TRIGGER customer_change AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW EXECUTE FUNCTION push_change();
