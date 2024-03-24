SET SESSION "myapp.reverse_trigger_off" = FALSE;

-- create function
CREATE or REPLACE FUNCTION create_or_update_event() RETURNS TRIGGER AS $$
    DECLARE
        payload json;
        reverse_trigger_off BOOLEAN;
    BEGIN

        SELECT current_setting('myapp.reverse_trigger_off')::BOOLEAN INTO reverse_trigger_off;

        IF reverse_trigger_off THEN
            RETURN NEW;
        end if;

        IF tg_op = 'DELETE' THEN
            payload := row_to_json(old);

            IF tg_table_name = 'stripe_integration' THEN
            DELETE FROM customers WHERE id=old.customer_id;
            end if;

        ELSE
            payload := row_to_json(new);
        END IF;



        PERFORM pg_notify('changes', json_build_array(tg_table_name, tg_op, payload)::text);
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

-- create trigger
CREATE TRIGGER customer_change AFTER INSERT OR UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION create_or_update_event();

CREATE TRIGGER stripe_change AFTER DELETE ON stripe_integration
    FOR EACH ROW EXECUTE FUNCTION create_or_update_event();