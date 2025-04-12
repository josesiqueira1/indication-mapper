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
    const DrugService = drugProto.drug.DrugService as any;

    const client = new DrugService(
      this.configService.get<string>('GRPC_SERVER_URL'),
      credentials.createInsecure(),
    );

    this.drugService = {
      getIndications: promisify(client.getIndications.bind(client)),
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