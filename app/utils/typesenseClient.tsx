import TypesenseInstantSearchAdapter from "typesense-instantsearch-adapter";

let typesenseClient: TypesenseInstantSearchAdapter | null = null;

export function getTypesenseClient() {
  if (!typesenseClient) {
    typesenseClient = new TypesenseInstantSearchAdapter({
      server: {
        apiKey: process.env.TYPESENSE_API_KEY!,
        nodes: [
          {
            host: process.env.TYPESENSE_HOST!,
            port: process.env.TYPESENSE_PORT!,
            protocol: process.env.TYPESENSE_PROTOCOL!,
          },
        ],
      },
    });
  }
  return typesenseClient;
}
