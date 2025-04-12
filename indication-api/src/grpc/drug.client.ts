import { Injectable, OnModuleInit } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { loadPackageDefinition, credentials } from '@grpc/grpc-js';
import { loadSync } from '@grpc/proto-loader';
import { join } from 'path';
import { promisify } from 'util';

interface DrugService {
  getIndications: (request: { setid: string }) => Promise<{
    indications: Array<{ code: string; description: string }>;
  }>;
}

@Injectable()
export class DrugClient implements OnModuleInit {
  private drugService: DrugService;

  constructor(private configService: ConfigService) {}

  onModuleInit() {
    const packageDefinition = loadSync(
      join(__dirname, '../proto/drug.proto'),
      {
        keepCase: true,
        longs: String,
        enums: String,
        defaults: true,
        oneofs: true,
      },
    );

    const drugProto = loadPackageDefinition(packageDefinition);
    const DrugMapper = (drugProto as any).drug_mapper.DrugMapper;

    const client = new DrugMapper(
      this.configService.get<string>('GRPC_SERVER_URL'),
      credentials.createInsecure(),
    );

    this.drugService = {
      getIndications: async ({ setid }) => {
        const response = await promisify(client.mapIndications.bind(client))({ set_id: setid });

        return {
          indications: response.icd10_mappings || [],
        };
      },
    };
  }

  async getIndications(setid: string) {
    try {
      const response = await this.drugService.getIndications({ setid });
      return response.indications;
    } catch (error) {
      console.error('Error calling gRPC service:', error);
      throw error;
    }
  }
}
