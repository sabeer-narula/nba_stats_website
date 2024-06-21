export interface Player {
  name: string;
  salary: number;
  overpaid_metric: number;
  best_stats: { [key: string]: number };
  worst_stats: { [key: string]: number };
}