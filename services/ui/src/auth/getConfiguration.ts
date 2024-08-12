import { Auth } from 'aws-amplify';

const getConfiguration = async () => {
	const session = await Auth.currentSession()
	const idToken = session.getIdToken()
	const configuration = {
		headers: {
			Authorization: idToken.getJwtToken(),
		}
	}

	return configuration
}

export { getConfiguration }