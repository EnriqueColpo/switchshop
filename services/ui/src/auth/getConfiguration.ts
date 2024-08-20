import { Auth } from 'aws-amplify';

const getConfiguration = async () => {
	const session = await Auth.currentSession()
	const idToken = session.getIdToken()
	const configuration = {
		headers: {
			Authorization: idToken.getJwtToken(),
			'Access-Control-Allow-Origin': '*'
		}
	}

	return configuration
}

export { getConfiguration }