CREATE TABLE "public"."datasets" ("id" uuid NOT NULL DEFAULT gen_random_uuid(), "name" text NOT NULL, "contact_id" uuid NOT NULL, "created_by" uuid NOT NULL, "maintained_by" uuid NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "updated_at" timestamptz NOT NULL DEFAULT now(), "dynamic_properties" jsonb NOT NULL, PRIMARY KEY ("id") , UNIQUE ("id"));COMMENT ON TABLE "public"."datasets" IS E'The category of information pertaining to a logical set of records.';
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
CREATE TRIGGER "set_public_datasets_updated_at"
BEFORE UPDATE ON "public"."datasets"
FOR EACH ROW
EXECUTE PROCEDURE "public"."set_current_timestamp_updated_at"();
COMMENT ON TRIGGER "set_public_datasets_updated_at" ON "public"."datasets"
IS 'trigger to set value of column "updated_at" to current timestamp on row update';
CREATE EXTENSION IF NOT EXISTS pgcrypto;
