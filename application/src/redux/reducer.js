import {Map} from 'immutable';
import {combineReducers} from 'redux-loop';
import NavigationStateReducer from '../modules/navigation/NavigationState';
import AuthStateReducer from '../modules/auth/AuthState';
import CounterStateReducer from '../modules/counter/CounterState';
import SessionStateReducer, {RESET_STATE} from '../modules/session/SessionState';
import HomepageStateReducer from '../modules/homepage/HomepageState';
import HomepageStateReducerCaregiver from '../modules/homepage-caregiver/HomepageState';
import JournalStateReducer from '../modules/journal/JournalState';
import StatusStateReducer from '../modules/status/StatusState';
import ActivitiesStateReducer from '../modules/activities/ActivitiesState';
import LoginStateReducer from '../modules/login/LoginState';
import OnboardingStateReducer from '../modules/onboarding/OnboardingState';
import PushNotificationsStateReducer from '../modules/push-notifications/PushNotificationsState';

const reducers = {
  // Authentication/login state
  auth: AuthStateReducer,

  // Counter sample app state. This can be removed in a live application
  counter: CounterStateReducer,

  // @NOTE: By convention, the navigation state must live in a subtree called
  //`navigationState`
  navigationState: NavigationStateReducer,

  session: SessionStateReducer,

  homepage: HomepageStateReducer,

  homepageCaregiver: HomepageStateReducerCaregiver,

  journal: JournalStateReducer,

  status: StatusStateReducer,

  activities: ActivitiesStateReducer,

  login: LoginStateReducer,

  onboarding: OnboardingStateReducer,

  pushNotifications: PushNotificationsStateReducer
};

// initial state, accessor and mutator for supporting root-level
// immutable data with redux-loop reducer combinator
const immutableStateContainer = Map();
const getImmutable = (child, key) => child ? child.get(key) : void 0;
const setImmutable = (child, key, value) => child.set(key, value);

const namespacedReducer = combineReducers(
  reducers,
  immutableStateContainer,
  getImmutable,
  setImmutable
);

export default function mainReducer(state, action) {
  if (action.type === RESET_STATE) {
    return namespacedReducer(action.payload, action);
  }

  return namespacedReducer(state || void 0, action);
}
