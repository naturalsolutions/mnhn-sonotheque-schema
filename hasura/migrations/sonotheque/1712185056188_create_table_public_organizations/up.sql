CREATE TABLE "public"."organizations" ("id" uuid NOT NULL DEFAULT gen_random_uuid(), "parent_id" uuid NOT NULL, "name" text NOT NULL, "type" text NOT NULL, "contact" text NOT NULL, "description" text NOT NULL, "dynamic_properties" jsonb NOT NULL, "located_in" uuid NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "updated_at" timestamptz NOT NULL DEFAULT now(), PRIMARY KEY ("id") , UNIQUE ("id"));COMMENT ON TABLE "public"."organizations" IS E'Institutions, units or organizations federating people';
CREATE OR REPLACE FUNCTION "public"."set_current_timestamp_updated_at"()
RETURNS TRIGGER AS $$
DECLARE
  _new record;
BEGIN
  _new := NEW;
  _new."updated_at" = NOW();
  RETURN _new;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER "set_public_organizations_updated_at"
BEFORE UPDATE ON "public"."organizations"
FOR EACH ROW
EXECUTE PROCEDURE "public"."set_current_timestamp_updated_at"();
COMMENT ON TRIGGER "set_public_organizations_updated_at" ON "public"."organizations"
IS 'trigger to set value of column "updated_at" to current timestamp on row update';
CREATE EXTENSION IF NOT EXISTS pgcrypto;
