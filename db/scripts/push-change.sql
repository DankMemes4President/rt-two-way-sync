CREATE or REPLACE FUNCTION push_change() RETURNS TRIGGER AS $$
    BEGIN
        PERFORM pg_notify('changes', tg_table_name || ',' || tg_op || ',' || new.id);
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;