-- create function
CREATE or REPLACE FUNCTION push_change() RETURNS TRIGGER AS $$
    BEGIN
        PERFORM pg_notify('changes', tg_table_name || ',' || tg_op || ',' || new.id);
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

-- create trigger
CREATE TRIGGER customer_change AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW EXECUTE FUNCTION push_change();
