import { Test, TestingModule } from '@nestjs/testing';
import { DrugsService } from './drugs.service';
import { getModelToken } from '@nestjs/mongoose';
import { Drug } from './schemas/drug.schema';
import { Model } from 'mongoose';

describe('DrugsService', () => {
  let service: DrugsService;
  let model: Model<Drug>;

  const mockDrug: Drug = {
    setid: '595f437d-2729-40bb-9c62-c8ece1f82780',
    name: 'Dupixent',
  };

  const mockDrugModel = {
    findOne: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        DrugsService,
        {
          provide: getModelToken(Drug.name),
          useValue: mockDrugModel,
        },
      ],
    }).compile();

    service = module.get<DrugsService>(DrugsService);
    model = module.get<Model<Drug>>(getModelToken(Drug.name));
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('findBySetid', () => {
    it('should return a drug by setid', async () => {
      const setid = '595f437d-2729-40bb-9c62-c8ece1f82780';
      jest.spyOn(model, 'findOne').mockResolvedValue(mockDrug);

      const result = await service.findBySetid(setid);
      expect(model.findOne).toHaveBeenCalledWith({ setid });
      expect(result).toEqual(mockDrug);
    });

    it('should return null when drug is not found', async () => {
      const setid = 'non-existent-setid';
      jest.spyOn(model, 'findOne').mockResolvedValue(null);

      const result = await service.findBySetid(setid);
      expect(model.findOne).toHaveBeenCalledWith({ setid });
      expect(result).toBeNull();
    });
  });
}); 