import { InfisicalSDK } from '@infisical/sdk';

const client = new InfisicalSDK({
  siteUrl: process.env.INFISICAL_URL || "https://app.infisical.com",
});

export const initializeInfisical = async () => {
  try {
    await client.auth().universalAuth.login({
      clientId: process.env.INFISICAL_CLIENT_ID!,
      clientSecret: process.env.INFISICAL_CLIENT_SECRET!
    });

    return client;
  } catch (error) {
    console.error('Failed to initialize Infisical:', error);
    throw error;
  }
};

export const getClerkSecrets = async () => {
  const infisicalClient = await initializeInfisical();
  
  try {
    const secrets = await infisicalClient.secrets().listSecrets({
      environment: process.env.NODE_ENV || 'development',
      projectId: process.env.INFISICAL_PROJECT_ID!,
      secretPath: "/clerk"
    });

    return {
      publishableKey: secrets.secrets.find(s => s.secretKey === 'NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY')?.secretValue,
      secretKey: secrets.secrets.find(s => s.secretKey === 'CLERK_SECRET_KEY')?.secretValue
    };
  } catch (error) {
    console.error('Failed to fetch Clerk secrets:', error);
    throw error;
  }
}; 