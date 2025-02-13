import { Component, OnInit } from '@angular/core';
import { FishingService } from '../services/fishing.service';
import { PlayerFishData, FishRecordBase } from '../services/fishing';
import { intervalToDuration } from 'date-fns';

// Define the three climates in the desired order
type Climate = 'Temperate' | 'Tropical' | 'Barren';

@Component({
  selector: 'app-fishing',
  templateUrl: './fishing.component.html',
  styleUrls: ['./fishing.component.css'],
})
export class FishingComponent implements OnInit {
  username: string = '';
  playerFishData?: PlayerFishData;
  errorMessage: string = '';
  lastUpdatedMinutes: number = 0;

  // Order of climates
  climates: Climate[] = ['Temperate', 'Tropical', 'Barren'];

  // Grouped records by climate
  groupedRecords: { [climate in Climate]: FishRecordBase[] } = {
    Temperate: [],
    Tropical: [],
    Barren: [],
  };

  constructor(private fishingService: FishingService) {}

  ngOnInit(): void {
    // Username is initially unset; waiting for user input.
  }

  fetchData(): void {
    const trimmedUsername: string = this.username.trim();
    if (trimmedUsername) {
      this.fishingService.getPlayerFishData(trimmedUsername).subscribe({
        next: (data: PlayerFishData) => {
          this.playerFishData = data;
          this.errorMessage = '';
          this.sortAndGroupRecords();
          this.updateLastUpdatedMinutes();
        },
        error: (error: Error) => {
          console.error('Error fetching data:', error);
          this.errorMessage =
            'Could not retrieve data. Make sure username is correct (case sensitive) and that the user has api access enabled.\nhttps://docs.islestats.net/user-guides/enable-mcci-api/';
          this.playerFishData = undefined;
          this.groupedRecords = {
            Temperate: [],
            Tropical: [],
            Barren: [],
          };
        },
      });
    }
  }

  private updateLastUpdatedMinutes(): void {
    if (this.playerFishData) {
      const now = new Date();
      const lastUpdated = new Date(this.playerFishData.last_updated);
      const duration = intervalToDuration({ start: lastUpdated, end: now });
      this.lastUpdatedMinutes = duration.minutes || 0;
    }
  }

  private sortAndGroupRecords(): void {
    if (!this.playerFishData) {
      return;
    }
    const records: FishRecordBase[] = this.playerFishData.fish_records.slice();

    const climateOrder: Record<Climate, number> = {
      Temperate: 0,
      Tropical: 1,
      Barren: 2,
    };
    const rarityOrder: Record<string, number> = {
      COMMON: 0,
      UNCOMMON: 1,
      RARE: 2,
      EPIC: 3,
      LEGENDARY: 4,
      MYTHIC: 5,
    };

    records.sort((a: FishRecordBase, b: FishRecordBase): number => {
      const climateA = a.fish_data.climate as Climate;
      const climateB = b.fish_data.climate as Climate;
      if (climateOrder[climateA] !== climateOrder[climateB]) {
        return climateOrder[climateA] - climateOrder[climateB];
      }
      const aCaught: boolean = a.weights.length > 0;
      const bCaught: boolean = b.weights.length > 0;
      if (aCaught !== bCaught) {
        return aCaught ? -1 : 1;
      }
      return rarityOrder[a.fish_data.rarity] - rarityOrder[b.fish_data.rarity];
    });

    this.groupedRecords = {
      Temperate: [],
      Tropical: [],
      Barren: [],
    };

    for (const record of records) {
      const climate = record.fish_data.climate as Climate;
      if (this.groupedRecords[climate] !== undefined) {
        this.groupedRecords[climate].push(record);
      }
    }
  }
}
