import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  input: '../local-service/generated/openapi.json',
  output: 'src/generated/client',
  client: 'fetch',
  schemas: false,
  services: {
    asClass: true,
  },
});
