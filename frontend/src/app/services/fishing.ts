export interface FishData {
  name: string;
  rarity: string;
  climate: string;
  collection: string;
  catchTime: string;
  elusive: boolean;
}

export interface FishWeight {
  weight: string;
  firstCaught: string;
}

export interface FishRecordBase {
  fish_data: FishData;
  weights: FishWeight[];
  isExpanded?: boolean;
}

export interface PlayerFishData {
  username: string;
  uuid: string;
  total_species: number;
  total_catches: number;
  last_updated: string | Date;
  fish_records: FishRecordBase[];
}
