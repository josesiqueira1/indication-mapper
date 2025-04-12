import { Test, TestingModule } from '@nestjs/testing';
import { MedicationsController } from './medications.controller';
import { MedicationsService } from './medications.service';
import { Medication } from './schemas/medication.schema';
import { FindBySetidDto } from './dto/find-by-setid.dto';
import { Types } from 'mongoose';

describe('MedicationsController', () => {
  let controller: MedicationsController;
  let service: MedicationsService;

  const mockMedication: Medication = {
    _id: new Types.ObjectId('507f1f77bcf86cd799439011'),
    setid: '595f437d-2729-40bb-9c62-c8ece1f82780',
    description: 'Dupixent (dupilumab) injection',
  };

  const mockMedicationsService = {
    findBySetid: jest.fn().mockResolvedValue(mockMedication),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [MedicationsController],
      providers: [
        {
          provide: MedicationsService,
          useValue: mockMedicationsService,
        },
      ],
    }).compile();

    controller = module.get<MedicationsController>(MedicationsController);
    service = module.get<MedicationsService>(MedicationsService);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('findBySetid', () => {
    it('should return a medication by setid', async () => {
      const findBySetidDto: FindBySetidDto = {
        setid: '595f437d-2729-40bb-9c62-c8ece1f82780',
      };

      const result = await controller.findBySetid(findBySetidDto);
      expect(service.findBySetid).toHaveBeenCalledWith(findBySetidDto.setid);
      expect(result).toEqual(mockMedication);
    });
  });
}); 