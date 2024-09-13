import { TestBed } from '@angular/core/testing';

import { HeightService } from './height.service';

describe('HeightService', () => {
  let service: HeightService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(HeightService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
