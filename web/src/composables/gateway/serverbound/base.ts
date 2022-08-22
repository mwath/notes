export interface IServerBound<Id extends string, Data extends {} = {}> {
  id: Id;
  data: Data;
}
