export const verifyToken = (req, res, next) => {
  const accessToken = req.headers.authorization;

  if (accessToken) {
    req.token = accessToken;
    next();
  } else {
    res.sendStatus(403);
  }
};

export const validateSignUp = (data) => {
  const { username, password } = data;
  if (!username || !password) { return false; }
  if (!username.match(/^\S+@\S+\.\S+$/)) { return false; }
  return true;
};
