import { Test, TestingModule } from '@nestjs/testing';
import { MedicationsService } from './medications.service';
import { getModelToken } from '@nestjs/mongoose';
import { Medication } from './schemas/medication.schema';
import { Model } from 'mongoose';

describe('MedicationsService', () => {
  let service: MedicationsService;
  let model: Model<Medication>;

  const mockMedication: Medication = {
    setid: '595f437d-2729-40bb-9c62-c8ece1f82780',
    description: 'Dupixent (dupilumab) injection',
  };

  const mockMedicationModel = {
    findOne: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        MedicationsService,
        {
          provide: getModelToken(Medication.name),
          useValue: mockMedicationModel,
        },
      ],
    }).compile();

    service = module.get<MedicationsService>(MedicationsService);
    model = module.get<Model<Medication>>(getModelToken(Medication.name));
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('findBySetid', () => {
    it('should return a medication by setid', async () => {
      const setid = '595f437d-2729-40bb-9c62-c8ece1f82780';
      jest.spyOn(model, 'findOne').mockResolvedValue(mockMedication);

      const result = await service.findBySetid(setid);
      expect(model.findOne).toHaveBeenCalledWith({ setid });
      expect(result).toEqual(mockMedication);
    });

    it('should return null when medication is not found', async () => {
      const setid = 'non-existent-setid';
      jest.spyOn(model, 'findOne').mockResolvedValue(null);

      const result = await service.findBySetid(setid);
      expect(model.findOne).toHaveBeenCalledWith({ setid });
      expect(result).toBeNull();
    });
  });
}); 