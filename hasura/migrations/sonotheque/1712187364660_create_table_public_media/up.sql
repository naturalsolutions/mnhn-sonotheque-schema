CREATE TABLE "public"."media" ("id" uuid NOT NULL DEFAULT gen_random_uuid(), "parent_id" uuid NOT NULL, "code" text NOT NULL, "title" text NOT NULL, "type" text NOT NULL, "subtype" text NOT NULL, "description" text NOT NULL, "tags" text[] NOT NULL, "comment" text NOT NULL, "resource_creation_technique" text NOT NULL, "available" daterange NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "updated_at" timestamptz NOT NULL DEFAULT now(), "recorded_at" timestamptz NOT NULL, "recording_range" tsrange NOT NULL, "duration" Numeric NOT NULL, "temporal" text NOT NULL, "time_of_day" text NOT NULL, "rating" integer NOT NULL, "naturality_rating" integer NOT NULL, "musicality_rating" integer NOT NULL, "media_propagation" text NOT NULL, "ecological_tags" text[] NOT NULL, "sampled_in" uuid NOT NULL, "occurs_at" uuid NOT NULL, "registered_in" uuid NOT NULL, "with_file" uuid NOT NULL, "created_by" uuid NOT NULL, "recorded_by" uuid NOT NULL, "provided_by" uuid NOT NULL, PRIMARY KEY ("id") , UNIQUE ("id"));COMMENT ON TABLE "public"."media" IS E'A media metadata description';
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
CREATE TRIGGER "set_public_media_updated_at"
BEFORE UPDATE ON "public"."media"
FOR EACH ROW
EXECUTE PROCEDURE "public"."set_current_timestamp_updated_at"();
COMMENT ON TRIGGER "set_public_media_updated_at" ON "public"."media"
IS 'trigger to set value of column "updated_at" to current timestamp on row update';
CREATE EXTENSION IF NOT EXISTS pgcrypto;
