import { Test, TestingModule } from '@nestjs/testing';
import { DrugsController } from './drugs.controller';
import { DrugsService } from './drugs.service';
import { Drug } from './schemas/drug.schema';
import { FindBySetidDto } from './dto/find-by-setid.dto';
import { Types } from 'mongoose';

describe('DrugsController', () => {
  let controller: DrugsController;
  let service: DrugsService;

  const mockDrug: Drug = {
    _id: new Types.ObjectId('507f1f77bcf86cd799439011'),
    setid: '595f437d-2729-40bb-9c62-c8ece1f82780',
    description: 'Dupixent (dupilumab) injection',
  };

  const mockDrugsService = {
    findBySetid: jest.fn().mockResolvedValue(mockDrug),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [DrugsController],
      providers: [
        {
          provide: DrugsService,
          useValue: mockDrugsService,
        },
      ],
    }).compile();

    controller = module.get<DrugsController>(DrugsController);
    service = module.get<DrugsService>(DrugsService);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('findBySetid', () => {
    it('should return a drug by setid', async () => {
      const findBySetidDto: FindBySetidDto = {
        setid: '595f437d-2729-40bb-9c62-c8ece1f82780',
      };

      const result = await controller.findBySetid(findBySetidDto);
      expect(service.findBySetid).toHaveBeenCalledWith(findBySetidDto.setid);
      expect(result).toEqual(mockDrug);
    });
  });
}); 